from django.db import models

class Departure(models.Model):

    hour = models.IntegerField()
    minute = models.IntegerField()
    direction = models.CharField(max_length=50)
    route = models.CharField(max_length=50)
    days = models.CharField(max_length=50)

    class Meta:
        verbose_name = "departure"
        verbose_name_plural = "departures"

    def __str__(self):
        return self.route

    def get_absolute_url(self):
        return reverse("departure_detail", kwargs={"pk": self.pk})
