



def test_dashboard(test_client):
    response=test_client.get('/dashboard')
    assert response.status_code==200