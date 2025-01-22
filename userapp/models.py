from django.db import models
# Create your models here.

class UserSignup(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)  # EmailField is more appropriate for email
    phone_number = models.CharField(max_length=15,unique=True)  # Assuming 15 chars for international numbers
    password = models.CharField(max_length=128)  # Increased max_length for password (consider hashing)

    class Meta:
        db_table = 'user_signup'