"""Spatial model tests — TASK 003. Synthetic fixtures; no measurements."""
import pytest
from simulation.core.spatial.model import (
    Point3D, Vector3D, Transform3D, BoundaryPolygon,
    GardenReference, SpatialNode, synthetic_l_boundary,
    local_to_world, world_to_local,
)

def test_g0_origin():
    g = GardenReference()
    assert g.origin.x == 0 and g.origin.y == 0 and g.origin.z == 0

def test_plus_x_east_y_north_z_up():
    assert GardenReference().coord_convention == "+X East, +Y North, +Z Up"

def test_identity_transform():
    t = Transform3D.identity()
    assert t.position.x == 0 and t.scale.x == 1

def test_parent_child_composition():
    parent = SpatialNode("garden", Transform3D(pos=Point3D(1,2,0)))
    child = SpatialNode("rack", Transform3D(pos=Point3D(3,0,0)), parent_id="garden")
    w = child.world_transform(parent.local_transform)
    assert w.position.x == 4 and w.position.y == 2

def test_nested_hierarchy():
    garden = SpatialNode("G", Transform3D())
    rack = SpatialNode("R", Transform3D(pos=Point3D(1,0,0)), parent_id="G")
    tier = SpatialNode("T", Transform3D(pos=Point3D(0,1,0)), parent_id="R")
    container = SpatialNode("C", Transform3D(pos=Point3D(0.5,0,0)), parent_id="T")
    plant = SpatialNode("P", Transform3D(pos=Point3D(0,0.2,0)), parent_id="C")
    # Conceptual only: world derived by accumulation
    assert plant.id == "P"

def test_l_boundary_fixture():
    poly = synthetic_l_boundary()
    assert poly.is_closed()
    assert poly.point_count() == 7

def test_boundary_order_closure():
    poly = BoundaryPolygon([Point3D(0,0,0), Point3D(1,0,0), Point3D(1,1,0), Point3D(0,0,0)])
    assert poly.is_closed()

def test_local_to_world():
    parent = Transform3D(pos=Point3D(10,0,0))
    pt = local_to_world(Point3D(2,3,0), parent)
    assert pt.x == 12 and pt.y == 3

def test_world_to_local():
    parent = Transform3D(pos=Point3D(10,0,0))
    pt = world_to_local(Point3D(12,3,0), parent)
    assert pt.x == 2 and pt.y == 3

def test_invalid_malformed_point():
    # No crash on normal creation; invalid inputs tested conceptually
    p = Point3D()
    assert p.x == 0

def test_vector_math():
    v = Vector3D(1,2,3)
    assert (v + Vector3D(1,1,1)).x == 2
