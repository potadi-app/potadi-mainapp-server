import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from .services import predict_disease

@pytest.mark.django_db
def test_disease_detection():
    client = APIClient()
    with open('tests/samples/healthy_leaf.jpg', 'rb') as image:
        response = client.post(reverse('disease-detection'), {'image': image}, format='multipart')

    assert response.status_code == status.HTTP_201_CREATED
    assert 'label' in response.data
    assert 'confidence' in response.data
    assert 'probabilities' in response.data
    assert 'healthy' in response.data['probabilities']
    assert 'early_blight' in response.data['probabilities']
    assert 'late_blight' in response.data['probabilities']
    assert 0 <= response.data['confidence'] <= 1


@pytest.mark.django_db
def test_detect_potato_disease():
    image = SimpleUploadedFile(name='test_image.jpg', content=open('tests/samples/healthy_leaf.jpg', 'rb').read(), content_type='image/jpeg')
    
    result = predict_disease(image)
    
    assert result['label'] in ['healthy', 'early blight', 'late blight']
    assert 0 <= result['confidence'] <= 1
