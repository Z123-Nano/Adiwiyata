"""Direct shadow — analytical vertical occluder on horizontal plane (TASK 009).
Convention: sun_direction vector points FROM sun TOWARD ground (downward component negative, horizontal opposite sun azimuth).
Shadow of vertical occluder falls AWAY from sun: shadow direction = sun_azimuth + 180° (mod 360).
Shadow length L = height / tan(altitude) when altitude > 0; else no shadow (sun below horizon).
No diffused/reflected/shadow-map; first layer only."""
from __future__ import annotations
import math
from simulation.core.shadow.model import SunDirection, ShadowResult, Occluder
from simulation.core.solar.model import SolarPosition

def sun_direction_from_solar(pos: SolarPosition) -> SunDirection:
    # Incoming sunlight direction: from sun to ground
    az_rad = math.radians(pos.azimuth_deg)
    alt_rad = math.radians(pos.altitude_deg)
    # Horizontal projection toward sun (from observer to sun) = (sin(az), cos(az))
    # Incoming sunlight = opposite: (-sin(az), -cos(az)) in (east, north)
    dx = -math.sin(az_rad)
    dy = -math.cos(az_rad)
    dz = -math.sin(math.radians(90 - pos.zenith_deg))  # downward; = -sin(alt) when alt small? Actually zenith = 90-alt -> dz = -cos(alt)? Simpler: dz = -math.sin(alt_rad) is wrong if alt=90 -> dz=-1 (down) correct; alt=0 -> dz=0. Actually sin(alt) at alt=90 is 1, so dz=-1 correct.
    # Correct: z component downward magnitude = sin(alt) (sun above) -> -sin(alt)
    dz = -math.sin(alt_rad)
    # Normalize to unit
    mag = math.sqrt(dx*dx + dy*dy + dz*dz)
    if mag > 0:
        dx, dy, dz = dx/mag, dy/mag, dz/mag
    return SunDirection(dx=dx, dy=dy, dz=dz, azimuth_deg=pos.azimuth_deg, altitude_deg=pos.altitude_deg)

def shadow_length_vertical_box(height_m: float, altitude_deg: float) -> float:
    if altitude_deg <= 0:
        return 0.0
    return height_m / math.tan(math.radians(altitude_deg))

def direct_shadow(occluder: Occluder, solar: SolarPosition, receiver_pos=None) -> ShadowResult:
    if solar.altitude_deg <= 0:
        return ShadowResult(sun_above_horizon=False, shadowed=False, notes="sun below horizon -> no direct shadow")
    # Analytical: vertical box casts shadow on horizontal plane along sun-azimuth-opposite
    L = shadow_length_vertical_box(occluder.height_m, solar.altitude_deg)
    # Shadow direction (projection on horizontal plane) = sun azimuth + 180
    shadow_dir = (solar.azimuth_deg + 180.0) % 360.0
    # Receiver check: if receiver is on ground plane within shadow extent along shadow direction from occluder base, shadowed.
    # Simplified: if receiver at same (x,y) as occluder base -> shadowed; if offset along direction > L -> not shadowed.
    shadowed = False
    if receiver_pos is not None:
        # receiver_pos = (x,y) ground; occluder base = (cx, cy)
        cx, cy = occluder.position[0], occluder.position[1]
        rx, ry = receiver_pos[0], receiver_pos[1]
        # Project receiver onto shadow line: distance along shadow direction
        dx = rx - cx
        dy = ry - cy
        # Shadow direction unit (east, north)
        dir_rad = math.radians(shadow_dir)
        dir_x = math.sin(dir_rad)  # east component of shadow direction
        dir_y = math.cos(dir_rad)  # north component
        proj = dx * dir_x + dy * dir_y
        # If projection positive and within L, shadowed; else not
        # Also require near line width (simplified: distance to line < occluder width ~ dims[0])
        perp = abs(dx * dir_y - dy * dir_x)
        width = occluder.dimensions[0] if len(occluder.dimensions) >= 1 else 0.5
        shadowed = (proj > -0.1) and (proj <= L + 0.1) and (perp < width/2 + 0.1)
    notes = f"shadow_len={L:.2f}m dir={shadow_dir:.1f}° (away from sun az={solar.azimuth_deg:.1f}°)"
    return ShadowResult(
        sun_above_horizon=True,
        occluder_id=occluder.id,
        receiver_id=None,
        shadowed=shadowed,
        shadow_length_m=round(L, 4) if L > 0 else None,
        shadow_direction_deg=round(shadow_dir, 2) if L > 0 else None,
        notes=notes,
    )
