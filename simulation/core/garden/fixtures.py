"""TASK 034 — real domain garden fixture (from domain contracts, not parallel API copy)."""
from simulation.core.contracts.domain import Garden, GardenReference, Boundary, SpatialObject, Plant

def synth_garden() -> Garden:
    ref = GardenReference(origin=[0,0,0], north_bearing_deg=0, coord_system="local-garden")
    boundary = Boundary(points=[[0,0,0],[4,0,0],[4,1,0],[2,1,0],[2,3,0],[0,3,0],[0,0,0]], type="polygon")
    # Real spatial objects derived from existing fixture hierarchy (TASK 005 / contracts)
    objects = [
        SpatialObject(id="b1", type="building", transform={"position":[-3.5,0.6,-2],"rotation_euler_deg":[0,0,0],"scale":[1.2,1.2,1.2],"parent_id":None}),
        SpatialObject(id="f1", type="fence", transform={"position":[-1,0,-4],"rotation_euler_deg":[0,90,0],"scale":[0.1,1.2,4],"parent_id":None}),
        SpatialObject(id="t1", type="tree", transform={"position":[-2,0.3,2],"rotation_euler_deg":[0,0,0],"scale":[0.4,0.6,0.4],"parent_id":None}),
        SpatialObject(id="rack1", type="rack", transform={"position":[1.5,0,1.5],"rotation_euler_deg":[0,11.5,0],"scale":[1.5,1.2,0.8],"parent_id":None}),
    ]
    # Real plant from architecture fixtures (TASK 017)
    plants = [
        Plant(id="plant-p1", species_id="demo-variety", variety_id="v1"),
    ]
    return Garden(id="garden-001", reference=ref, boundary=boundary, objects=[o.id for o in objects], provenance="TASK_034 synthetic domain fixture")

def synth_spatial_objects() -> list[SpatialObject]:
    return synth_garden().__dict__["objects"]  # not direct; instead return fixture objects

# Direct object list (used by service)
SYNTH_SPATIAL = [
    SpatialObject(id="b1", type="building", transform={"position":[-3.5,0.6,-2],"rotation_euler_deg":[0,0,0],"scale":[1.2,1.2,1.2],"parent_id":None}),
    SpatialObject(id="f1", type="fence", transform={"position":[-1,0,-4],"rotation_euler_deg":[0,90,0],"scale":[0.1,1.2,4],"parent_id":None}),
    SpatialObject(id="t1", type="tree", transform={"position":[-2,0.3,2],"rotation_euler_deg":[0,0,0],"scale":[0.4,0.6,0.4],"parent_id":None}),
    SpatialObject(id="rack1", type="rack", transform={"position":[1.5,0,1.5],"rotation_euler_deg":[0,11.5,0],"scale":[1.5,1.2,0.8],"parent_id":None}),
    SpatialObject(id="tier1", type="tier", transform={"position":[0,0,0],"rotation_euler_deg":[0,0,0],"scale":[1,0.15,1],"parent_id":"rack1"}),
    SpatialObject(id="tier2", type="tier", transform={"position":[0,0.45,0],"rotation_euler_deg":[0,0,0],"scale":[1,0.15,1],"parent_id":"rack1"}),
    SpatialObject(id="c1", type="container", transform={"position":[-0.3,0.15,0],"rotation_euler_deg":[0,0,0],"scale":[0.35,0.2,0.35],"parent_id":"tier1"}),
]
