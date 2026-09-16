"""LightField computation — TASK 011. Domain-only; no R3F/Three.js."""
from __future__ import annotations
from simulation.core.light.contracts import LightComponents
from simulation.core.light.approximation import diffuse_approximation, reflected_approximation, combined_light
from simulation.core.shadow.direct import direct_shadow
from simulation.core.shadow.model import Occluder
from simulation.core.solar.model import SolarPosition
from simulation.core.light.field.contracts import LightSample, LightField

def compute_lightfield(
    solar: SolarPosition,
    grid_bounds: tuple[float, float, float, float],  # xmin, xmax, ymin, ymax
    grid_res: tuple[int, int] = (10, 10),
    z_height: float = 0.0,
    occluders: list = None,
) -> LightField:
    """Regular horizontal grid at fixed z; direct evaluated per point via shadow logic."""
    if grid_res[0] <= 0 or grid_res[1] <= 0:
        raise ValueError("grid resolution must be positive")
    xmin, xmax, ymin, ymax = grid_bounds
    x_step = (xmax - xmin) / max(grid_res[0] - 1, 1)
    y_step = (ymax - ymin) / max(grid_res[1] - 1, 1)
    samples = []
    occluders = occluders or []
    for i in range(grid_res[0]):
        for j in range(grid_res[1]):
            x = xmin + i * x_step
            y = ymin + j * y_step
            # Direct: if sun below horizon => 0; else check occluders (simplified: first occluder only for first layer)
            direct = 1.0 if solar.above_horizon else 0.0
            # Shadow check simplified: point inside shadow of any occluder -> direct 0 (approx)
            shadowed = False
            if solar.above_horizon:
                for occ in occluders:
                    res = direct_shadow(occ, solar, receiver_pos=(x, y, z_height))
                    if res.shadowed:
                        shadowed = True
                        break
            if shadowed:
                direct = 0.0
            # Diffuse: daylight * sky visibility; use full visibility for open scene
            diff_approx = diffuse_approximation(1.0, solar.altitude_deg)
            # Reflected: simple synthetic surface reflectance ~0.2, visible 1.0, incident = direct + diffuse
            refl_approx = reflected_approximation(0.2, 1.0, min(1.0, direct + diff_approx.diffuse_output), coeff=0.3)
            total = direct + diff_approx.diffuse_output + refl_approx.reflected_output
            samples.append(LightSample(x=x, y=y, z=z_height, direct=direct, diffuse=diff_approx.diffuse_output, reflected=refl_approx.reflected_output, total=total))
    return LightField(
        extent_min=(xmin, ymin, z_height),
        extent_max=(xmax, ymax, z_height),
        resolution=(grid_res[0], grid_res[1], 1),
        samples=samples,
        sampling_strategy="regular_grid_horizontal",
        solar_reference=solar.timestamp.isoformat() if solar.timestamp else None,
    )
