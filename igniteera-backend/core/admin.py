

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, Profile, Assessment, LearningModule, LearningPlan, Article, ContactSubmission, Activity

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ("username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("username", "email")

admin.site.register(Profile)
admin.site.register(Assessment)
admin.site.register(LearningModule)
admin.site.register(LearningPlan)
admin.site.register(Article)
admin.site.register(ContactSubmission)
admin.site.register(Activity)
