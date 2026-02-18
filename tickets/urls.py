from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TicketClassifyView, TicketStatsView, TicketViewSet

router = DefaultRouter()
router.register(r"", TicketViewSet, basename="ticket")

urlpatterns = [
    path("stats/", TicketStatsView.as_view(), name="ticket-stats"),
    path("classify/", TicketClassifyView.as_view(), name="ticket-classify"),
    path("", include(router.urls)),
]
