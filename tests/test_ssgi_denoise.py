import pytest
import math
from render import ssgi_denoise as mod

CASES = [
    ("bounce", 'm.secondary_bounce(0.5, 0.8) == approx(0.4)'),
    ("rays", 'm.ray_count(0.5, 8) == 4'),
    ("reproj", 'm.reproject_validate(0.5, 0.55, 0.1) is True'),
    ("bilat", 'm.bilateral(0.05, 0.8, 0.1, 0.5) == 1.0'),
    ("edge", 'm.upsample_edge(0.1, 0.2) is True'),
    ("diffuse", 'm.separate_diffuse(1, 0.5) == approx(0.5)'),
    ("fallback", 'm.offscreen_fallback((1.2, 0.5), 0.3) == 0.3'),
    ("hdr", 'm.hdr_clamp(1200, 1000) == 1000'),
    ("probe", 'm.probe_priority(0.5) == approx(0.5)'),
    ("cam", 'm.camera_key("L") == "L"'),
    ("sum", 'm.radiance_sum(1, 2) == 3'),
    ("foot", 'm.screen_footprint(2, 0.5) == approx(1.0)'),
    ("atten", 'm.bounce_attenuation(0.5, 2) == approx(0.25)'),
    ("uv", 'm.valid_uv((0.5, 0.5)) is True'),
    ("id", 'm.ssgi_id(3, 2) == "3:2"')
]

@pytest.mark.parametrize("name,expr", CASES, ids=[c[0] for c in CASES])
def test_contract(name, expr):
    assert eval(expr, {"m": mod, "approx": pytest.approx, "math": math})
