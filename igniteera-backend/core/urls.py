from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (UserViewSet, ProfileViewSet, AssessmentViewSet, LearningModuleViewSet,
                    LearningPlanViewSet, ArticleViewSet, ContactViewSet, ActivityViewSet, generate_roadmap)

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"profiles", ProfileViewSet)
router.register(r"assessments", AssessmentViewSet)
router.register(r"modules", LearningModuleViewSet)
router.register(r"plans", LearningPlanViewSet)
router.register(r"articles", ArticleViewSet)
router.register(r"contact", ContactViewSet)
router.register(r"activities", ActivityViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("generate_roadmap/", generate_roadmap),
]
