from datetime import date

def test_only_organizers_can_create_ticket(client, organizer, event, organizer_token):
    headers = {
        "Authorization": f"Bearer {organizer_token}"
    }

    data = {
        "expiration_date": event.date, # setting the expiration date to be the date of the event
        "price": 0
    }

    response = client.post(f"/events/{event.id}/tickets", json=data,  headers=headers)
    assert response.status_code == 201

def test_only_organizers_cannot_create_invalid_expiration_date(client, event, organizer_token):
    headers = {
        "Authorization": f"Bearer {organizer_token}"
    }

    data = {
        "expiration_date": date.today(), # setting the expiration date to be the date of the event
        "price": 100
    }

    response = client.post(f"/events/{event.id}/tickets", json=data,  headers=headers)
    assert response.status_code == 400
    assert response.json() == {"detail": "Expiration date must be less than the event date"}