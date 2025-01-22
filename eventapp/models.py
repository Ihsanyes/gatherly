from django.db import models
from userapp.models import UserSignup

class Service(models.Model):
    name = models.CharField(max_length=255)
    class Meta:
        db_table = 'service'

# Create your models here.
class CreateEvent(models.Model):
    create_title = models.CharField(max_length=255)
    established_in = models.IntegerField()  # Removed max_length
    contact = models.CharField(max_length=15)  # Increased length for potential international numbers
    wh_number = models.CharField(max_length=15)  # Increased length
    address = models.CharField(max_length=255)
    event_photos = models.ImageField(upload_to='image/',null=True)  # Corrected the path for image uploads
    select_services = models.ManyToManyField(Service, related_name='events')
    rating = models.FloatField(null=True)  # For Top Rated
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True)  # For Price sorting
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255,null=True)

    creator = models.ForeignKey(UserSignup,on_delete=models.CASCADE,related_name='event_user',null=True)
    

    class Meta:
        db_table = 'create_events'

class EventImage(models.Model):
    event = models.ForeignKey(CreateEvent, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='event_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'event_images'
