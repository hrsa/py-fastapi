




def test_root(client):
    res = client.get('/')
    assert res.status_code == 200
    assert res.json().get("message") == "Hello sun!"


def test_hello(client):
    res = client.get('/hello/TestingClient')
    assert res.status_code == 200
    assert res.json().get("message") == "Hello, my dear TestingClient! How are you today?"
