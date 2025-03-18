from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import AbstractUser, Group ,Permission

from django.utils.translation import gettext as _

class CustomUser(AbstractUser):
    mobile_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)

    # Add or change related_name for groups and user_permissions fields
    groups = models.ManyToManyField(Group, verbose_name=_('groups'), blank=True, related_name='customuser_set', related_query_name='user')
    user_permissions = models.ManyToManyField(Permission, verbose_name=_('user permissions'), blank=True, related_name='customuser_set', related_query_name='user')

    def __str__(self):
        return self.username



class Mechanic(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='mechanic_photos/', null=True, blank=True)
    mobile=models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.CharField(max_length=1000,blank=True)  # Make the url field optional
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url



class RepairRequest(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    )

    requested_by = models.ForeignKey(User, on_delete=models.CASCADE)
    mechanic = models.ForeignKey('Mechanic', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    location = models.OneToOneField('Location', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Repair request by {self.requested_by.username}"

class ProblemSubmission(models.Model):
    name = models.CharField(max_length=100)
    vehicle_number = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    problem_statement = models.TextField()
    bill = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Feedback(models.Model):
    RATING_CHOICES = (
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    )
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating: {self.rating}"

