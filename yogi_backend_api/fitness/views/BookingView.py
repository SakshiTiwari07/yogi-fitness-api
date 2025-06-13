from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import transaction
from fitness.models.FitnessClassModel import FitnessClass
from fitness.models.BookingModel import Booking
from fitness.serializers.BookingSerializer import BookingSerializer

import logging
logger = logging.getLogger(__name__)

class CreateBookingView(APIView):
    """
    API view to handle creation of a new booking for a fitness class.
    Ensures:
    - class exists
    - slots are available
    - atomic transaction during slot update and booking creation
    """

    def post(self, request):
        # Extract required fields from request
        class_id = request.data.get('class_id')
        client_name = request.data.get('client_name')
        client_email = request.data.get('client_email')

        # Basic validation
        if not all([class_id, client_name, client_email]):
            return Response(
                {'error': 'class_id, client_name, and client_email are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Ensure the class exists
        fitness_class = get_object_or_404(FitnessClass, id=class_id)

        # Check slot availability
        if fitness_class.available_slots <= 0:
            return Response({'error': 'No available slots'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Ensure atomicity in case of concurrency
            with transaction.atomic():
                # Safely reduce available slots
                fitness_class.available_slots -= 1
                fitness_class.save()

                # Create the booking
                booking = Booking.objects.create(
                    fitness_class=fitness_class,
                    client_name=client_name,
                    client_email=client_email
                )

                logger.info(f"Booking created for {client_email} in class {fitness_class.id}")

                # Serialize and return created booking
                serializer = BookingSerializer(booking)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Booking failed: {str(e)}")
            return Response({'error': 'Booking could not be created.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BookingListByEmailView(APIView):
    """
    API view to retrieve all bookings for a given client email.
    Useful for client-side session history or management.
    """

    def get(self, request):
        # Get email from query parameters
        email = request.query_params.get('email')
        
        # Validate email presence
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch all bookings with matching client email
        bookings = Booking.objects.filter(client_email=email)
        serializer = BookingSerializer(bookings, many=True)

        logger.info(f"Fetched {len(bookings)} bookings for {email}")
        return Response(serializer.data, status=status.HTTP_200_OK)
