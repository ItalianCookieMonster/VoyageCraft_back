import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from itinerary.models import Itinerary, ItineraryStep
from users_app.models import User
from destinations.models import Destination

@pytest.mark.django_db
def test_create_itinerary():
    """
    Prueba la creación de un itinerario mediante una solicitud POST a la API.

    **Given** un usuario autenticado y un destino creado.
    **When** el usuario envía una solicitud POST para crear un itinerario con los datos proporcionados.
    **Then** se debe crear el itinerario y devolver un código de estado 201 (Creado).
    """
    client = APIClient()

    # Given: Crear un usuario y autenticar
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.force_authenticate(user=user)

    # Given: Crear un destino
    destination = Destination.objects.create(name="Test Destination", description="A test destination")

    url = reverse('itinerary-create')  # Asegúrate de que este nombre coincida con el nombre de la URL
    data = {
        "user": user.id,
        "name": "My Test Itinerary",
        "description": "This is a test itinerary.",
        "start_date": "2024-09-01",
        "end_date": "2024-09-07",
        "destination": destination.id,
        "steps": [
            {
                "description": "Arrive at the beach",
                "date": "2024-09-01",
                "order": 1
            }
        ]
    }

    # When: Enviar una solicitud POST para crear un itinerario
    response = client.post(url, data, format='json')

    # Then: Verificar que el itinerario se ha creado correctamente
    assert response.status_code == status.HTTP_201_CREATED
    assert Itinerary.objects.count() == 1
    assert Itinerary.objects.get().name == "My Test Itinerary"


@pytest.mark.django_db
def test_get_itinerary_detail():
    """
    Prueba la obtención de los detalles de un itinerario mediante una solicitud GET a la API.

    **Given** un usuario autenticado, un destino y un itinerario creado.
    **When** el usuario envía una solicitud GET para obtener los detalles del itinerario.
    **Then** se debe devolver el detalle del itinerario con un código de estado 200 (OK).
    """
    user = User.objects.create_user(username='testuser', password='testpassword')
    destination = Destination.objects.create(name="Test Destination", description="A test destination")
    itinerary = Itinerary.objects.create(
        user=user,
        name="My Test Itinerary",
        description="A simple test.",
        start_date="2024-09-01",
        end_date="2024-09-07",
        destination=destination
    )
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('itinerary-detail', args=[itinerary.id])

    # When: Enviar una solicitud GET para obtener los detalles del itinerario
    response = client.get(url, format='json')

    # Then: Verificar que los detalles del itinerario se obtienen correctamente
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == "My Test Itinerary"


@pytest.mark.django_db
def test_create_itinerary_step():
    """
    Prueba la creación de un paso en un itinerario mediante una solicitud POST a la API.

    **Given** un usuario autenticado, un destino y un itinerario creado.
    **When** el usuario envía una solicitud POST para agregar un paso al itinerario.
    **Then** se debe crear el paso y devolver un código de estado 201 (Creado).
    """
    user = User.objects.create_user(username='testuser', password='testpassword')
    destination = Destination.objects.create(name="Test Destination", description="A test destination")
    itinerary = Itinerary.objects.create(
        user=user,
        name="My Test Itinerary",
        description="A simple test.",
        start_date="2024-09-01",
        end_date="2024-09-07",
        destination=destination
    )
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('itinerarystep-create', args=[itinerary.id])
    data = {
        "description": "Step 1",
        "date": "2024-09-02",
        "order": 1
    }

    # When: Enviar una solicitud POST para agregar un paso al itinerario
    response = client.post(url, data, format='json')

    # Then: Verificar que el paso se ha creado correctamente
    assert response.status_code == status.HTTP_201_CREATED
    assert ItineraryStep.objects.count() == 1
    assert ItineraryStep.objects.get().description == "Step 1"


@pytest.mark.django_db
def test_update_itinerary_step():
    """
    Prueba la actualización de un paso en un itinerario mediante una solicitud PATCH a la API.

    **Given** un usuario autenticado, un destino, un itinerario y un paso.
    **When** el usuario envía una solicitud PATCH para actualizar el paso del itinerario.
    **Then** se debe actualizar el paso y devolver un código de estado 200 (OK).
    """
    user = User.objects.create_user(username='testuser', password='testpassword')
    destination = Destination.objects.create(name="Test Destination", description="A test destination")
    itinerary = Itinerary.objects.create(
        user=user,
        name="My Test Itinerary",
        description="A simple test.",
        start_date="2024-09-01",
        end_date="2024-09-07",
        destination=destination
    )
    step = ItineraryStep.objects.create(
        itinerary=itinerary,
        description="Original Step",
        date="2024-09-02",
        order=1
    )
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('itinerarystep-detail', args=[step.id])
    data = {
        "description": "Updated Step",
        "date": "2024-09-03",
        "order": 2
    }

    # When: Enviar una solicitud PATCH para actualizar el paso del itinerario
    response = client.patch(url, data, format='json')

    # Then: Verificar que el paso se ha actualizado correctamente
    assert response.status_code == status.HTTP_200_OK
    step.refresh_from_db()
    assert step.description == "Updated Step"
    assert step.date == "2024-09-03"
    assert step.order == 2


@pytest.mark.django_db
def test_delete_itinerary_step():
    """
    Prueba la eliminación de un paso en un itinerario mediante una solicitud DELETE a la API.

    **Given** un usuario autenticado, un destino, un itinerario y un paso.
    **When** el usuario envía una solicitud DELETE para eliminar el paso del itinerario.
    **Then** se debe eliminar el paso y devolver un código de estado 204 (Sin Contenido).
    """
    user = User.objects.create_user(username='testuser', password='testpassword')
    destination = Destination.objects.create(name="Test Destination", description="A test destination")
    itinerary = Itinerary.objects.create(
        user=user,
        name="My Test Itinerary",
        description="A simple test.",
        start_date="2024-09-01",
        end_date="2024-09-07",
        destination=destination
    )
    step = ItineraryStep.objects.create(
        itinerary=itinerary,
        description="Step to be deleted",
        date="2024-09-02",
        order=1
    )
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('itinerarystep-detail', args=[step.id])

    # When: Enviar una solicitud DELETE para eliminar el paso del itinerario
    response = client.delete(url, format='json')

    # Then: Verificar que el paso se ha eliminado correctamente
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert ItineraryStep.objects.count() == 0
