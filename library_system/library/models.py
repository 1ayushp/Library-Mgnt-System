from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('librarian', 'Librarian'),
        ('member', 'Member'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    rented_books = models.ManyToManyField('Book', blank=True, related_name='renters')
    
    def __str__(self):
        return f"{self.username} ({self.role})"

    def save(self, *args, **kwargs):
        # Automatically assign staff to admin and role admin to superuser
        if self.is_superuser:
            self.role = 'admin'
            self.is_staff = True  

        elif self.role == 'admin':
            self.is_staff = True 
            self.is_superuser = False 

        else:
            self.is_staff = False
            self.is_superuser = False

        super().save(*args, **kwargs)
        if self.role == 'admin':
            # Allows created admin with Books permissions
            content_type = ContentType.objects.get_for_model(Book)
            perms = Permission.objects.filter(content_type=content_type)
            self.user_permissions.set(perms)


class Book(models.Model):
    title = models.CharField(max_length=200,null=False,blank=False,unique=True)
    author = models.CharField(max_length=100)
    published_date = models.DateField()

    def __str__(self):
        return self.title
