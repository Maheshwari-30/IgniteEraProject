from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, ProfileViewSet, AssessmentViewSet, LearningModuleViewSet,
    LearningPlanViewSet, ArticleViewSet, ContactViewSet, ActivityViewSet,
    generate_roadmap, home_view, api_root
)

# Create router for REST API endpoints
router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"profiles", ProfileViewSet)
router.register(r"assessments", AssessmentViewSet)
router.register(r"modules", LearningModuleViewSet)
router.register(r"plans", LearningPlanViewSet)
router.register(r"articles", ArticleViewSet)
router.register(r"contact", ContactViewSet)
router.register(r"activities", ActivityViewSet)

# Combine everything into urlpatterns
urlpatterns = [
    path("", home_view, name="home"),                   # Homepage (HTML)
    path("api/", api_root, name="api_root"),            # API root (JSON summary)
    path("api/v1/", include(router.urls)),              # All your REST API routes
    path("api/generate_roadmap/", generate_roadmap),    # AI roadmap endpoint
]
