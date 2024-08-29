import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from itinerary.models import Itinerary, ItineraryStep


#crear
@pytest.mark.django_db
def test_create_itinerary():
    client = APIClient()
    url = reverse('create_itinerary')
    data = {
        "name": "My Test Itinerary",
        "description": "This is a test itinerary."
    }

    response = client.post(url, data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert Itinerary.objects.count() == 1
    assert Itinerary.objects.get().name == "My Test Itinerary"



@pytest.mark.django_db
def test_get_itinerary_detail():
    itinerary = Itinerary.objects.create(name="My Test Itinerary", description="A simple test.")
    client = APIClient()
    url = reverse('itinerary_detail', args=[itinerary.id])

    response = client.get(url, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == "My Test Itinerary"


@pytest.mark.django_db
def test_create_itinerary_step():
    itinerary = Itinerary.objects.create(name="My Test Itinerary", description="A simple test.")
    client = APIClient()
    url = reverse('create_itinerary_step', args=[itinerary.id])
    data = {
        "step_name": "Step 1",
        "step_description": "This is the first step."
    }

    response = client.post(url, data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert ItineraryStep.objects.count() == 1
    assert ItineraryStep.objects.get().step_name == "Step 1"

    @pytest.mark.django_db
    def test_create_itinerary_step():
        itinerary = Itinerary.objects.create(name="My Test Itinerary", description="A simple test.")
        client = APIClient()
        url = reverse('create_itinerary_step', args=[itinerary.id])
        data = {
            "step_name": "Step 1",
            "step_description": "This is the first step."
        }

        response = client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert ItineraryStep.objects.count() == 1
        assert ItineraryStep.objects.get().step_name == "Step 1"