def test_animal_report(client):
    # Test GET request to retrieve the animal report
    response = client.get('/reports/animals')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_visitor_report(client):
    # Test GET request to retrieve the visitor report
    response = client.get('/reports/visitors')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert 'ticket_type' in response.json[0]

def test_revenue_report(client):
    # Test GET request to retrieve the revenue report
    response = client.get('/reports/revenue')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert 'revenue' in response.json[0]
