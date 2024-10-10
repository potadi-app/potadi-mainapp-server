from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import DiagnoseSerializer
from .services import predict_disease_saved_model
from .models import Diagnose
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class DiagnoseViewSetAPI(viewsets.ViewSet):
    parser_classes = (MultiPartParser, FormParser)
    
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: DiagnoseSerializer(many=True)},
        operation_description="Retrieve a list of disease predictions.",
        operation_summary="List Disease Predictions",
        tags=['Disease Detection']
    )
    def list(self, request):
        predictions = Diagnose.objects.filter(user=request.user).order_by('-created_at')
        paginator = PageNumberPagination()
        paginator.page_size = 25
        result_page = paginator.paginate_queryset(predictions, request)
        serializer = DiagnoseSerializer(result_page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: DiagnoseSerializer(),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description="Prediction not found",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status': openapi.Schema(type=openapi.TYPE_STRING, description='Status response'),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Error message'),
                    },
                )
            ),
        },
        operation_description="Retrieve a single disease prediction.",
        operation_summary="Get Disease Prediction",
        tags=['Disease Detection']
    )
    def retrieve(self, request, pk=None):
        try:
            prediction = Diagnose.objects.get(user=request.user, uuid=pk)
            serializer = DiagnoseSerializer(prediction, context={'request': request})
            return Response(serializer.data)
        except Diagnose.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Prediction not found'
            }, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='image',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                required=True,
                description='Image file to upload'
            ),
        ],
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="Disease detected successfully",
                schema=DiagnoseSerializer()
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Invalid input",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status': openapi.Schema(type=openapi.TYPE_STRING, description='Status response'),
                        'message': openapi.Schema(type=openapi.TYPE_OBJECT, description='Error messages'),
                    },
                )
            ),
        },
        operation_description="Detect potato leaf disease from an uploaded image.",
        operation_summary="Detect Potato Leaf Disease",
        tags=['Disease Detection']
    )
    def create(self, request):
        serializer = DiagnoseSerializer(data=request.data)
        if serializer.is_valid():
            image_data = request.FILES.get('image')
            
            detection_result = predict_disease_saved_model(image=image_data)
            
            prediction = Diagnose.objects.create(
                user=request.user,
                image=image_data,
                label=detection_result['label'],
                confidence=detection_result['confidence'],
                details=detection_result['details']
            )
            response_serializer = DiagnoseSerializer(prediction, context={'request': request})
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 'error',
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
    @swagger_auto_schema(
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response(
                description="Prediction successfully deleted",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status': openapi.Schema(type=openapi.TYPE_STRING, description='Status response'),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message'),
                    },
                )
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description="Prediction not found",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status': openapi.Schema(type=openapi.TYPE_STRING, description='Status response'),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Error message'),
                    },
                )
            ),
        },
        operation_description="Delete a single disease prediction.",
        operation_summary="Delete Disease Prediction",
        tags=['Disease Detection']
    )
    
    def destroy(self, request, pk=None):
        try:
            prediction = Diagnose.objects.get(user=request.user, id=pk)
            prediction.delete()
            return Response({
                    'status': 'success',
                    'message': 'Prediction successfully deleted'
                }, status=status.HTTP_204_NO_CONTENT)
        except Diagnose.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Prediction not found'
            }, status=status.HTTP_404_NOT_FOUND)
