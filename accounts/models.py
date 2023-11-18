
from django.contrib.auth.models import AbstractUser, Permission,Group
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.models import User

# Your code utilizing Django models goes here
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog_images', blank=True, null=True)
    category = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
                return self.title



class User(AbstractUser):
    # Your custom fields and methods here

    class Meta:
        permissions = [
            ("custom_permission", "Custom Permission Description"),
            # Define any other permissions if needed
        ]
        default_permissions = ()

    # Provide unique related names for user_permissions and groups fields
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        related_name='custom_user_permissions',  # Unique related name
        blank=True,
    )
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        related_name='custom_user_groups',  # Unique related name
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )


class Subscription(models.Model):
    PLAN_CHOICES = [
        ('Basic', 'Basic'),
        ('Premium', 'Premium'),
        # Add other plan options here
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=50, choices=PLAN_CHOICES)
    active = models.BooleanField(default=False)
    posts_allowed = models.IntegerField(default=1)  # Default for Basic

    def save(self, *args, **kwargs):
        if self.plan == 'Premium':
            self.posts_allowed = -1  # Premium subscription allows unlimited posts
        super().save(*args, **kwargs)
