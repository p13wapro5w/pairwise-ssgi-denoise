"""SSGI 追踪 / 降噪管线的纯函数实现。

修复点对应 README 中的十个问题：
- secondary_bounce / bounce_attenuation：二次反弹按反照率衰减，不再按常数补能量；
- screen_footprint / ray_count：射线数按像素足迹（深度相关）分配；
- reproject_validate：时域重投影做深度校验，拒绝不一致的历史辐照度；
- bilateral：双边权重在颜色差之外增加法线项，相反法线的面不再被糊在一起；
- upsample_edge：半分辨率上采样按深度差保边，消除墙角光晕；
- separate_diffuse：金属度拆分漫反射/镜面，两路分别积分，能量不翻倍；
- offscreen_fallback / valid_uv：屏幕外的像素回退到探针数据；
- hdr_clamp / radiance_sum：HDR 全链路，累加不提前 clamp；
- probe_priority：探针按视角朝向优先级更新；
- camera_key / ssgi_id：多相机历史按相机 id 隔离。
"""


def secondary_bounce(first, albedo):
    """二次反弹。

    一次反弹辐照度打到新表面后，被该表面反照率反射的部分即二次反弹，
    取代原先的常数能量补偿。
    """
    return first * albedo


def ray_count(footprint, base):
    """射线分配。

    按像素足迹比例分配射线数（足迹越大、覆盖的世界空间范围越大，
    需要的射线越多），保证至少发射 1 条，返回整数。
    """
    return max(1, int(base * footprint))


def reproject_validate(prev, cur, threshold):
    """重投影校验。

    比较重投影位置的历史深度与当前深度，深度差不超过阈值才接受
    上一帧的辐照度，否则丢弃历史（角色走过墙面时不再残留亮斑）。
    """
    return abs(cur - prev) <= threshold


def bilateral(color_delta, normal_dot, ct, nt):
    """双边权重。

    颜色门：颜色差不超过颜色阈值 ct；
    法线门：法线点积不低于法线阈值 nt（朝向相反的面权重为 0）。
    两项同时通过权重才为 1，否则为 0。
    """
    color_weight = 1.0 if color_delta <= ct else 0.0
    normal_weight = 1.0 if normal_dot >= nt else 0.0
    return color_weight * normal_weight


def upsample_edge(delta, threshold):
    """上采样保边。

    半分辨率追踪结果上采样时，比较相邻深度差：深度差在阈值内说明
    属于同一表面（返回 True，允许混合），超出阈值视为深度边缘，
    必须保边，避免墙角光晕。
    """
    return abs(delta) <= threshold


def separate_diffuse(energy, metallic):
    """漫反射分离。

    金属表面没有漫反射分量，入射能量按 (1 - metallic) 划入漫反射路，
    其余划入镜面路，两路分别积分，避免漫反射探针与屏幕空间结果
    直接相加造成能量翻倍。
    """
    return energy * (1.0 - metallic)


def offscreen_fallback(uv, probe):
    """屏幕外回退。

    UV 落在屏幕外时屏幕空间追踪无效，回退返回探针辐照度；
    UV 合法时回退贡献为 0，由调用方使用屏幕空间结果。
    """
    if not valid_uv(uv):
        return probe
    return 0.0


def hdr_clamp(value, maximum):
    """HDR 限幅。

    仅在缓冲入口做上限保护（写缓冲时的硬上限），累加阶段不允许
    提前 clamp，以保留霓虹灯等高亮光源的 HDR 能量。
    """
    return min(value, maximum)


def probe_priority(dot):
    """探针优先级。

    以探针朝向与视线方向的点积作为更新优先级：正对点积越大优先级
    越高，背对相机的探针（负点积）优先级为 0，快速转身时面前的
    墙面探针优先刷新，颜色不再滞后。
    """
    return max(0.0, float(dot))


def camera_key(camera):
    """多相机键。

    为每个相机返回独立的历史缓冲键，分屏 / 瞄准镜相机不再共用
    主视图的 SSGI 历史。
    """
    if isinstance(camera, str):
        return camera
    for attr in ("name", "id", "camera_id"):
        key = getattr(camera, attr, None)
        if key is not None:
            return key
    return str(camera)


def radiance_sum(a, b):
    """辐照度叠加。

    HDR 链路中的辐照度直接相加，不做 clamp，保证高亮间接光不发灰。
    """
    return a + b


def screen_footprint(depth, angle):
    """像素足迹。

    像素在世界空间中的投影足迹随深度增长，并按表面角度系数缩放，
    供射线分配使用：远处像素足迹大、分到更多射线，解决近处过采样、
    远处欠采样。
    """
    return depth * angle


def bounce_attenuation(albedo, bounces):
    """多次反弹衰减。

    每经过一次反弹能量乘以反照率，n 次反弹后衰减为 albedo ** n。
    """
    return albedo ** bounces


def valid_uv(uv):
    """UV 合法性。

    两个分量都落在 [0, 1] 内才是屏幕内 UV。
    """
    return all(0.0 <= component <= 1.0 for component in uv)


def ssgi_id(seed, index):
    """SSGI id。

    由随机种子与射线序号组成唯一标识，用于每条射线的历史 / 降噪记录。
    """
    return f"{seed}:{index}"
