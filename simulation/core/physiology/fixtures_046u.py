"""TASK 046U fixtures — synthetic LightField pairs for SpatialPPFDTransferFactor derivation."""
from simulation.core.light.field.contracts import LightSample, LightField
from simulation.core.physiology.derive_spatial_transfer import derive_spatial_transfer_from_lightfield

# A — compatible pair, total, same solar/approx, positive denominator (transfer > 0)
ref_A = LightField(
    samples=[LightSample(x=0.0,y=0.0,direct=0.6,diffuse=0.3,reflected=0.1,total=1.0)],
    solar_reference="t1", approximation_params={"approximation":"synthetic_clear_day","sky_vis":"high"},
    simulation_time_ref="t1",
)
tgt_A = LightField(
    samples=[LightSample(x=1.0,y=0.0,direct=0.3,diffuse=0.15,reflected=0.05,total=0.5)],
    solar_reference="t1", approximation_params={"approximation":"synthetic_clear_day","sky_vis":"high"},
    simulation_time_ref="t1",
)
# B — mismatched approximation (normalization context differs → blocked)
ref_B = LightField(samples=[LightSample(x=0,y=0,direct=0.6,diffuse=0.3,reflected=0.1,total=1.0)], solar_reference="t1", approximation_params={"approximation":"a1"}, simulation_time_ref="t1")
tgt_B = LightField(samples=[LightSample(x=1,y=0,direct=0.3,diffuse=0.15,reflected=0.05,total=0.5)], solar_reference="t1", approximation_params={"approximation":"a2"}, simulation_time_ref="t1")
# C — zero denominator (reference total 0) → blocked at derivation (reference itself ok per 046T)
ref_C = LightField(samples=[LightSample(x=0,y=0,direct=0,diffuse=0,reflected=0,total=0)], solar_reference="t1", approximation_params={}, simulation_time_ref="t1")
tgt_C = LightField(samples=[LightSample(x=1,y=0,direct=0.3,diffuse=0.15,reflected=0.05,total=0.5)], solar_reference="t1", approximation_params={}, simulation_time_ref="t1")
