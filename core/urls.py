
from django.urls import path
from .views import PingView, CallbackView, DecodeVinView  # ✅ Add DecodeVinView import

urlpatterns = [
    path("ping/", PingView.as_view(), name="ping"),
    path("callback/", CallbackView.as_view(), name="callback"),
    path("decode-vin/", DecodeVinView.as_view(), name="decode_vin"),  # ✅ Add this route
]
