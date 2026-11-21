import math

def secondary_bounce(first, albedo):
    """二次反弹。"""
    raise NotImplementedError("TODO: secondary_bounce")

def ray_count(footprint, base):
    """射线分配。"""
    raise NotImplementedError("TODO: ray_count")

def reproject_validate(prev, cur, threshold):
    """重投影校验。"""
    raise NotImplementedError("TODO: reproject_validate")

def bilateral(color_delta, normal_dot, ct, nt):
    """双边权重。"""
    raise NotImplementedError("TODO: bilateral")

def upsample_edge(delta, threshold):
    """上采样保边。"""
    raise NotImplementedError("TODO: upsample_edge")

def separate_diffuse(energy, metallic):
    """漫反射分离。"""
    raise NotImplementedError("TODO: separate_diffuse")

def offscreen_fallback(uv, probe):
    """屏幕外回退。"""
    raise NotImplementedError("TODO: offscreen_fallback")

def hdr_clamp(value, maximum):
    """HDR 限幅。"""
    raise NotImplementedError("TODO: hdr_clamp")

def probe_priority(dot):
    """探针优先级。"""
    raise NotImplementedError("TODO: probe_priority")

def camera_key(camera):
    """多相机键。"""
    raise NotImplementedError("TODO: camera_key")

def radiance_sum(a, b):
    """辐照度叠加。"""
    raise NotImplementedError("TODO: radiance_sum")

def screen_footprint(depth, angle):
    """像素足迹。"""
    raise NotImplementedError("TODO: screen_footprint")

def bounce_attenuation(albedo, bounces):
    """多次反弹衰减。"""
    raise NotImplementedError("TODO: bounce_attenuation")

def valid_uv(uv):
    """UV 合法性。"""
    raise NotImplementedError("TODO: valid_uv")

def ssgi_id(seed, index):
    """SSGI id。"""
    raise NotImplementedError("TODO: ssgi_id")
