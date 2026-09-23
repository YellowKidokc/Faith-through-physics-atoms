from fastapi.testclient import TestClient


def test_status_returns_ok():
    from api_server.main import app
    client = TestClient(app)
    response = client.get("/api/status")
    assert response.status_code == 200
    assert response.json()["ok"] is True


def test_papers_lists_sample_paper(monkeypatch, tmp_path):
    from api_server.main import app
    import canon_store.paper as paper_module

    monkeypatch.setattr(paper_module, "CANON_STORE_ROOT", tmp_path)
    record = paper_module.create_paper("sources/sample.md", "sha256:abc", title="Sample")
    paper_module.save_paper(record)

    client = TestClient(app)
    response = client.get("/api/papers")
    assert response.status_code == 200
    uuids = [p["uuid"] for p in response.json()["papers"]]
    assert record["address"]["uuid"] in uuids


def test_get_paper_returns_record(monkeypatch, tmp_path):
    from api_server.main import app
    import canon_store.paper as paper_module

    monkeypatch.setattr(paper_module, "CANON_STORE_ROOT", tmp_path)
    record = paper_module.create_paper("sources/sample.md", "sha256:abc", title="Sample")
    paper_module.save_paper(record)

    client = TestClient(app)
    response = client.get(f"/api/paper/{record['address']['uuid']}")
    assert response.status_code == 200
    assert response.json()["address"]["uuid"] == record["address"]["uuid"]


def test_run_endpoint_queues_run(monkeypatch, tmp_path):
    from api_server.main import app
    import canon_store.paper as paper_module

    monkeypatch.setattr(paper_module, "CANON_STORE_ROOT", tmp_path)
    record = paper_module.create_paper("sources/sample.md", "sha256:abc", title="Sample")
    paper_module.save_paper(record)

    client = TestClient(app)
    response = client.post("/api/run", json={
        "paper_uuid": record["address"]["uuid"],
        "stations": ["atoms"],
        "provider": "deepseek",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "queued"
    assert data["paper_uuid"] == record["address"]["uuid"]
    assert "run_id" in data
