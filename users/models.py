from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    birthdate = models.DateField(null=True, blank=True)
    registration_source = models.CharField(
        max_length=20,
        choices=(
            ('local', 'Local'),
            ('google', 'Google'),
            ('facebook', 'Facebook'),
        ),
        default='local',
    )

    def __str__(self):
        return self.username
