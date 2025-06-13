from django.urls import path
from fitness.views.FitnessClassView import FitnessClassAPIView
from fitness.views.BookingView import CreateBookingView, BookingListByEmailView

urlpatterns = [
    path('classes/', FitnessClassAPIView.as_view(), name='fitness-class-api'),
    path('bookings/', CreateBookingView.as_view(), name='create-booking'),
    path('bookings/by-email/', BookingListByEmailView.as_view(), name='bookings-by-email'),
]
