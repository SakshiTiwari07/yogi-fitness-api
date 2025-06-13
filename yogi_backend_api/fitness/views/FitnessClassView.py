from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from fitness.models.FitnessClassModel import FitnessClass
from fitness.serializers.FitnessClassSerializer import FitnessClassSerializer
import logging

# Setup logging to capture important events and errors
logger = logging.getLogger(__name__)

class FitnessClassAPIView(APIView):
    """
    API View to handle GET and POST requests for FitnessClass.
    GET - Returns all available fitness classes.
    POST - Creates a new fitness class entry.
    """

    def get(self, request):
        """
        Handle GET request to fetch all fitness classes.
        """
        try:
            classes = FitnessClass.objects.all()
            serializer = FitnessClassSerializer(classes, many=True)
            logger.info(f"Fetched {len(classes)} fitness classes.")
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            # Log and return a server error response if fetching fails
            logger.error(f"Error fetching fitness classes: {str(e)}")
            return Response({'error': 'Could not retrieve classes.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """
        Handle POST request to create a new fitness class.
        Expects JSON body with class details.
        """
        serializer = FitnessClassSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                # Save the new fitness class
                serializer.save()
                logger.info("New fitness class created.")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                # Log and return a server error if save fails
                logger.error(f"Error creating fitness class: {str(e)}")
                return Response({'error': 'Failed to create class.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            # Return validation errors with a bad request status
            logger.warning(f"Validation error: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
