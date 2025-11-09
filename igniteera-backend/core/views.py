from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Profile, Assessment, LearningModule, LearningPlan, Article, ContactSubmission, Activity
from .serializers import (
    UserSerializer, RegisterSerializer, ProfileSerializer,
    AssessmentSerializer, LearningModuleSerializer, LearningPlanSerializer,
    ArticleSerializer, ContactSerializer, ActivitySerializer
)
import datetime

User = get_user_model()

# ----------------------------------------------------------
# ✅ NEW — Homepage (HTML) + Root API (JSON)
# ----------------------------------------------------------

def home_view(request):
    """Renders your HTML home page"""
    return render(request, "core/home.html")


def api_root(request):
    """Returns basic API info as JSON"""
    data = {
        "project": "IgniteEra Backend API",
        "message": "Welcome to IgniteEra Backend API 🚀",
        "status": "success",
        "environment": "development",
        "endpoints": {
            "admin": "/admin/",
            "api_root": "/api/",
            "auth_login_logout": "/api/auth/",
            "auth_registration": "/api/auth/registration/",
            "token_obtain": "/api/token/",
            "token_refresh": "/api/token/refresh/",
        },
        "credits": "Developed by IgniteEra Team ⚡",
    }
    return JsonResponse(data)


# ----------------------------------------------------------
# 🔹 Your existing API ViewSets remain unchanged below
# ----------------------------------------------------------

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == "admin"


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["post"], permission_classes=[permissions.AllowAny])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": UserSerializer(user).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }, status=status.HTTP_201_CREATED)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.select_related("user").all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ("admin", "mentor"):
            return Profile.objects.all()
        return Profile.objects.filter(user=user)


class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer
    permission_classes = [permissions.IsAuthenticated]


class LearningModuleViewSet(viewsets.ModelViewSet):
    queryset = LearningModule.objects.all()
    serializer_class = LearningModuleSerializer
    permission_classes = [IsAdminOrReadOnly]


class LearningPlanViewSet(viewsets.ModelViewSet):
    queryset = LearningPlan.objects.all()
    serializer_class = LearningPlanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ("admin", "mentor"):
            return LearningPlan.objects.all()
        return LearningPlan.objects.filter(user=user)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAdminOrReadOnly]


class ContactViewSet(viewsets.ModelViewSet):
    queryset = ContactSubmission.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.AllowAny]


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def generate_roadmap(request):
    """
    Placeholder AI roadmap endpoint.
    Accepts: { optional: 'user_id' or activity data } and returns a LearningPlan
    """
    user = request.user
    modules = LearningModule.objects.all()[:10]
    items = []
    for i, m in enumerate(modules[:5]):
        items.append({
            "module_id": m.id,
            "title": m.title,
            "due_date": (datetime.date.today() + datetime.timedelta(days=i+1)).isoformat(),
            "status": "assigned"
        })
    plan = LearningPlan.objects.create(user=user, title="Auto Roadmap", items=items)
    return Response({"plan_id": plan.id, "items": items})
