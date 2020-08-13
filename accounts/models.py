from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    # date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to="users/%Y%m%d",
                              blank=True)


    def __str__(self):
        return f'profile of {self.user}'


class EmailList(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return self.email 