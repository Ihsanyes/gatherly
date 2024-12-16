from django.db import models

# Create your models here.
class CreateEvent(models.Model):
    create_title = models.CharField(max_length=255)
    established_in = models.IntegerField()  # Removed max_length
    contact = models.CharField(max_length=15)  # Increased length for potential international numbers
    wh_number = models.CharField(max_length=15)  # Increased length
    address = models.CharField(max_length=255)
    services = models.TextField()  # Changed to TextField for more flexibility
    event_photos = models.ImageField(upload_to='images/')  # Corrected the path for image uploads

    class Meta:
        db_table = 'create_event'
