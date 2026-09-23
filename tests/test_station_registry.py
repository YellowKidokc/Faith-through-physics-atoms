from stations.registry import list_stations, get_station, get_run_order


def test_registry_has_atoms():
    stations = list_stations()
    assert any(s["id"] == "atoms" for s in stations)


def test_run_order_respects_dependencies():
    order = get_run_order(["paper_grader"])
    assert order.index("atoms") < order.index("paper_grader")
