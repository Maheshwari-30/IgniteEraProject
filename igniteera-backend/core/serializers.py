from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile, Assessment, LearningModule, LearningPlan, Article, ContactSubmission, Activity

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "role"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ["username", "email", "password", "role"]

    def create(self, validated_data):
        pw = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(pw)
        user.save()
        Profile.objects.create(user=user)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = "__all__"


class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = "__all__"


class LearningModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningModule
        fields = "__all__"


class LearningPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningPlan
        fields = "__all__"


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSubmission
        fields = "__all__"


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = "__all__"
