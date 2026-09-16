"""Garden spatial model — domain-level. No Three.js. Synthetic fixtures only."""
from __future__ import annotations
from typing import List, Optional, Tuple

class Point3D:
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.x = x; self.y = y; self.z = z
    def __repr__(self): return f"Point3D({self.x},{self.y},{self.z})"
    def to_tuple(self) -> Tuple[float,float,float]: return (self.x, self.y, self.z)

class Vector3D:
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.x = x; self.y = y; self.z = z
    def __add__(self, o: Vector3D) -> Vector3D: return Vector3D(self.x+o.x, self.y+o.y, self.z+o.z)
    def __sub__(self, o: Vector3D) -> Vector3D: return Vector3D(self.x-o.x, self.y-o.y, self.z-o.z)
    def scale(self, s: float) -> Vector3D: return Vector3D(self.x*s, self.y*s, self.z*s)

class Transform3D:
    """Local transform: position + rotation (euler xyz deg) + scale."""
    def __init__(self, pos: Optional[Point3D]=None, rot: Optional[Point3D]=None, scale: Optional[Point3D]=None):
        self.position = pos or Point3D()
        self.rotation = rot or Point3D()
        self.scale = scale or Point3D(1,1,1)
    def identity() -> Transform3D:
        return Transform3D()

class BoundaryPolygon:
    """Ordered points; closure validated separately."""
    def __init__(self, points: List[Point3D]):
        self.points = points
    def is_closed(self) -> bool:
        if not self.points: return False
        first = self.points[0]
        last = self.points[-1]
        return abs(first.x-last.x)<1e-6 and abs(first.y-last.y)<1e-6 and abs(first.z-last.z)<1e-6
    def point_count(self) -> int: return len(self.points)

class GardenReference:
    def __init__(self, id: str = "G0", description: str = "local origin", north_bearing_deg: float = 0.0):
        self.id = id
        self.description = description
        self.origin = Point3D(0,0,0)
        self.north_bearing_deg = north_bearing_deg
        self.coord_convention = "+X East, +Y North, +Z Up"

class SpatialNode:
    """Parent-child spatial node. Local + derived world transform conceptually separate."""
    def __init__(self, id: str, local_transform: Transform3D, parent_id: Optional[str]=None):
        self.id = id
        self.local_transform = local_transform
        self.parent_id = parent_id
    def world_transform(self, parent_world: Optional[Transform3D]=None) -> Transform3D:
        # Simplified: local + parent world (no rotation decomposition yet)
        p = parent_world or Transform3D.identity()
        # Conceptual only: position addition; full rotation/scale composition deferred
        combined_pos = Point3D(
            p.position.x + self.local_transform.position.x,
            p.position.y + self.local_transform.position.y,
            p.position.z + self.local_transform.position.z,
        )
        return Transform3D(pos=combined_pos, rot=self.local_transform.rotation, scale=self.local_transform.scale)

def local_to_world(local: Point3D, parent_world: Transform3D) -> Point3D:
    # Domain-level: add parent position; scale not applied to point here
    return Point3D(
        parent_world.position.x + local.x,
        parent_world.position.y + local.y,
        parent_world.position.z + local.z,
    )

def world_to_local(world: Point3D, parent_world: Transform3D) -> Point3D:
    return Point3D(
        world.x - parent_world.position.x,
        world.y - parent_world.position.y,
        world.z - parent_world.position.z,
    )

def synthetic_l_boundary() -> BoundaryPolygon:
    """Synthetic L-shaped polygon — not real measurements."""
    return BoundaryPolygon([
        Point3D(0,0,0), Point3D(4,0,0), Point3D(4,1,0),
        Point3D(2,1,0), Point3D(2,3,0), Point3D(0,3,0), Point3D(0,0,0)
    ])
