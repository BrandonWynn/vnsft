from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny  # ✅ Import this for public endpoints
from .serializers import PingSerializer
import logging
import json

logger = logging.getLogger(__name__)

class PingView(APIView):
    """
    GET /api/ping/  → returns {"message": "pong"}
    """
    permission_classes = [AllowAny]  # ✅ Optional: make /ping/ open too

    def get(self, request):
        serializer = PingSerializer({"message": "pong"})
        return Response(serializer.data, status=status.HTTP_200_OK)


class CallbackView(APIView):
    """
    GET /api/callback/  → Handles Manheim OAuth redirect (?code=abc123 or ?error=access_denied)
    POST /api/callback/ → Handles Manheim webhooks (e.g., JSON payload for auction updates)
    """
    permission_classes = [AllowAny]  # ✅ Make this public — required for Manheim callbacks

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        """Handle OAuth redirect"""
        code = request.query_params.get('code')
        error = request.query_params.get('error')
        if error:
            logger.error(f"Manheim API error: {error}")
            return Response(
                {"error": f"Manheim choked: {error}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        logger.info(f"Got OAuth code: {code}")
        return Response(
            {"message": "OAuth callback received. You’re tapping out the API!"},
            status=status.HTTP_200_OK
        )

    def post(self, request):
        """Handle webhook payload"""
        try:
            data = request.data
            logger.info(f"Webhook data: {data}")
            return Response(
                {"message": "Webhook received. Smooth submission!"},
                status=status.HTTP_200_OK
            )
        except json.JSONDecodeError:
            logger.error("Invalid webhook JSON")
            return Response(
                {"error": "Bad JSON, try again"},
                status=status.HTTP_400_BAD_REQUEST
            )
