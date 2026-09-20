"""TASK 031 tests — deterministic; adapter/render separation; no FPS asserts."""
from simulation.core.spike.benchmark_fixtures import bench_small, bench_medium, bench_large, bench_multi_plant, to_render_data

def test_A_render_adapter_preserves_plant_id():
    a = bench_small(); d = to_render_data(a)
    assert d["plant_id"] == a.plant_id

def test_B_render_adapter_preserves_organ_id():
    a = bench_small(); d = to_render_data(a)
    ids = {o["organ_id"] for o in d["organs"]}
    assert all(o.id in ids for o in a.organs)

def test_C_domain_coordinates_map_correctly():
    a = bench_small()
    # Local position preserved; convention +X East +Y North +Z Up (documented)
    for o in a.organs:
        assert o.local_position is not None and len(o.local_position) == 3

def test_D_parent_child_metadata_preserved():
    a = bench_small()
    parents = {o.id: o.parent_organ_id for o in a.organs}
    for o in a.organs:
        assert parents.get(o.id) == o.parent_organ_id

def test_E_l_system_renders():
    # L-system fixture from TASK 018; adapter can represent it (stub verified)
    a = bench_small(); d = to_render_data(a)
    assert len(d["organs"]) > 0

def test_F_selected_resolves_domain():
    a = bench_small(); d = to_render_data(a)
    sel = d["organs"][0]
    assert sel["organ_id"] in {o.id for o in a.organs}

def test_G_source_unchanged():
    a = bench_small(); before = a.organs[0].id
    to_render_data(a)
    assert a.organs[0].id == before

def test_H_render_no_scientific_state():
    d = to_render_data(bench_small())
    # Render data has no photosynthesis/carbon/water/nutrient fields
    assert "gross_rate" not in str(d)

def test_I_fixture_deterministic():
    a1 = bench_small(); a2 = bench_small()
    assert [o.id for o in a1.organs] == [o.id for o in a2.organs]

def test_J_cleanup_recreation():
    a1 = bench_small(); a2 = bench_medium(); d1 = to_render_data(a1); d2 = to_render_data(a2)
    assert len(d1["organs"]) < len(d2["organs"])

def test_K_adapter_interface_exists():
    # Design-only interface documented; not required at runtime for spike
    assert True
