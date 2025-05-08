from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('guest', 'Guest'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    institution = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    join_date = models.DateField(auto_now_add=True)
    last_login = models.DateField(auto_now=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class ResearchPaper(models.Model):
    ACCESS_CHOICES = [
        ('open', 'Open'),
        ('restricted', 'Restricted'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    journal = models.CharField(max_length=255)
    publication_date = models.DateField(null=True, blank=True)
    authors = models.ManyToManyField("Author", through="PaperAuthor")
    keywords = models.ManyToManyField("Keyword", through="PaperKeyword")
    access_setting = models.CharField(max_length=10, choices=ACCESS_CHOICES)
    file_url = models.URLField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    file_id = models.CharField(max_length=255, blank=True, null=True)

class Dataset(models.Model):
    ACCESS_CHOICES = [
        ('open', 'Open'),
        ('restricted', 'Restricted'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    version = models.CharField(max_length=50)
    size = models.DecimalField(max_digits=10, decimal_places=2)
    file_url = models.URLField()
    # preview_url = models.URLField()
    access_setting = models.CharField(max_length=10, choices=ACCESS_CHOICES)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

class Request(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paper = models.ForeignKey(ResearchPaper, on_delete=models.SET_NULL, null=True, blank=True)
    dataset = models.ForeignKey(Dataset, on_delete=models.SET_NULL, null=True, blank=True)
    purpose = models.CharField(max_length=255)
    reason_for_access = models.TextField()
    request_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

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
    request = models.ForeignKey(Request, on_delete=models.CASCADE, null=True, blank=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'admin'})
    action = models.CharField(max_length=10, choices=[('approved', 'Approved'), ('rejected', 'Rejected')])
    timestamp = models.DateTimeField(auto_now_add=True)
