from django.db import models
from django.contrib.auth.models import AbstractUser

# Extend the User model to include additional fields
class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('guest', 'Guest'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    avatar = models.URLField(blank=True, null=True)
    institution = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    join_date = models.DateField(auto_now_add=True)
    last_login = models.DateField(blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class ResearchPaper(models.Model):
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    publication_details = models.TextField()
    access_setting = models.CharField(max_length=10, choices=[('open', 'Open'), ('restricted', 'Restricted')])
    file_url = models.URLField()
    preview_url = models.URLField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_papers')

class Dataset(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    version = models.CharField(max_length=50)
    size = models.DecimalField(max_digits=10, decimal_places=2)
    file_url = models.URLField()
    preview_url = models.URLField()
    access_setting = models.CharField(max_length=10, choices=[('open', 'Open'), ('restricted', 'Restricted')])
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_datasets')

class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paper = models.ForeignKey(ResearchPaper, on_delete=models.SET_NULL, null=True, blank=True)
    dataset = models.ForeignKey(Dataset, on_delete=models.SET_NULL, null=True, blank=True)
    purpose = models.CharField(max_length=255)
    reason_for_access = models.TextField()
    request_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')])

class Author(models.Model):
    name = models.CharField(max_length=255)
    affiliation = models.CharField(max_length=255)

class PaperAuthor(models.Model):
    paper = models.ForeignKey(ResearchPaper, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

class DatasetAuthor(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

class Category(models.Model):
    name = models.CharField(max_length=255)

class Keyword(models.Model):
    term = models.CharField(max_length=255)

class PaperKeyword(models.Model):
    paper = models.ForeignKey(ResearchPaper, on_delete=models.CASCADE)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)

class DatasetKeyword(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)

class PermissionChangeLog(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_logs')
    action = models.CharField(max_length=10, choices=[('approved', 'Approved'), ('rejected', 'Rejected')])
    timestamp = models.DateTimeField(auto_now_add=True)
