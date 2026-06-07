def test_health_check(client):
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "message": "ok",
        "data": {"status": "ok"},
    }
