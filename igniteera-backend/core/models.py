from django.db import models
from django.contrib.auth.models import AbstractUser

# Choices for user roles
ROLE_CHOICES = (
    ("student", "Student"),
    ("mentor", "Mentor"),
    ("admin", "Admin"),
)

# Custom User model
class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return f"{self.username} ({self.email})"


# Profile model (linked one-to-one with User)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    age = models.PositiveIntegerField(null=True, blank=True)
    grade = models.CharField(max_length=50, blank=True)
    interests = models.JSONField(default=list, blank=True)
    skill_vector = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile: {self.user.username}"


# Assessment model
class Assessment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assessments")
    title = models.CharField(max_length=255)
    results = models.JSONField(default=dict)  # e.g. {"topic1": 80, "topic2": 90}
    score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Assessment: {self.title} - {self.user.username}"


# Learning module model
class LearningModule(models.Model):
    title = models.CharField(max_length=255)
    summary = models.TextField(blank=True)
    content = models.TextField(blank=True)  # markdown or HTML content
    estimated_minutes = models.IntegerField(default=15)
    tags = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.title


# Learning plan model
class LearningPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="learning_plans")
    title = models.CharField(max_length=255)
    items = models.JSONField(default=list)  # [{module_id, due_date, status}]
    progress = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} for {self.user.username}"


# Articles or blog posts
class Article(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title


# Contact form submissions
class ContactSubmission(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"


# User activity tracking
class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="activities")
    module = models.ForeignKey(LearningModule, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, default="assigned")
    due_date = models.DateField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Activity of {self.user.username} - {self.status}"
