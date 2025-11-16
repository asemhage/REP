from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AmenityViewSet,
    HallViewSet,
    HallSlotViewSet,
    PropertyAvailabilityViewSet,
    PropertyViewSet,
)

router = DefaultRouter()
router.register(r"amenities", AmenityViewSet, basename="amenity")
router.register(r"properties", PropertyViewSet, basename="property")
router.register(r"property-availability", PropertyAvailabilityViewSet, basename="property-availability")
router.register(r"halls", HallViewSet, basename="hall")

urlpatterns = [
    path("", include(router.urls)),
    path("halls/<int:hall_pk>/slots/", HallSlotViewSet.as_view({"get": "list"}), name="hall-slots"),
]

