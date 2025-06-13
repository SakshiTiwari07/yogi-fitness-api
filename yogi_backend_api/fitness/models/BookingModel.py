from django.db import models
# from fitness.models.FitnessClassModel import FitnessClass


class Booking(models.Model):
    fitness_class = models.ForeignKey('FitnessClass', on_delete=models.CASCADE, related_name='bookings')
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()

    def __str__(self):
        return f"{self.client_name} - {self.fitness_class.name}"
