
from django.urls import path
from .views import PingView, CallbackView

urlpatterns = [
    path("ping/", PingView.as_view(), name="ping"),
    path("callback/", CallbackView.as_view(), name="callback"),
]