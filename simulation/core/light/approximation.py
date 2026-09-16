"""Light approximation — TASK 010. No lux/PPFD; relative normalized; approximation only."""
from __future__ import annotations
from simulation.core.light.contracts import DiffuseApproximation, ReflectedApproximation, LightComponents

def diffuse_approximation(sky_visibility: float, solar_altitude_deg: float, clear_baseline: float = 1.0) -> DiffuseApproximation:
    # Night => daylight_factor = 0 => diffuse = 0 regardless of sky visibility
    daylight = 1.0 if solar_altitude_deg > 0 else 0.0
    visibility = max(0.0, min(1.0, sky_visibility))
    out = daylight * visibility * clear_baseline
    return DiffuseApproximation(
        sky_visibility_fraction=visibility,
        daylight_factor=daylight,
        diffuse_output=out,
        daylight_baseline=clear_baseline,
    )

def reflected_approximation(reflectance: float, visible_frac: float, incident_env: float, coeff: float = 0.3) -> ReflectedApproximation:
    # Bounded: coeff <= 1, reflectance <= 1, visible <= 1, incident <= 1 => out <= 1
    reflectance = max(0.0, min(1.0, reflectance))
    visible_frac = max(0.0, min(1.0, visible_frac))
    incident_env = max(0.0, min(1.0, incident_env))
    coeff = max(0.0, min(1.0, coeff))
    out = reflectance * visible_frac * incident_env * coeff
    return ReflectedApproximation(
        surface_reflectance=reflectance,
        visible_surface_fraction=visible_frac,
        incident_environmental=incident_env,
        reflection_coefficient=coeff,
        reflected_output=out,
    )

def combined_light(direct: float, diffuse_approx: DiffuseApproximation, reflected_approx: ReflectedApproximation) -> LightComponents:
    # Direct given by shadow/direct model (relative 0-1); diffuse/reflected from approximations
    direct = max(0.0, min(1.0, direct))
    total = direct + diffuse_approx.diffuse_output + reflected_approx.reflected_output
    return LightComponents(
        direct=direct,
        diffuse=diffuse_approx.diffuse_output,
        reflected=reflected_approx.reflected_output,
        total=total,
    )
