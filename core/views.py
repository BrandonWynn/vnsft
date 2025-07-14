from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny  # ✅ For public endpoints
from .serializers import PingSerializer
import logging
import json
import requests
from django.http import HttpResponse

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


class DecodeVinView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        html_form = """
            <html>
            <body>
                <h2>VIN Decoder Test</h2>
                <form method="post">
                    <label for="vin">Enter VIN:</label>
                    <input type="text" name="vin" id="vin" />
                    <button type="submit">Decode</button>
                </form>
            </body>
            </html>
        """
        return HttpResponse(html_form)

    def post(self, request):
        vin = request.data.get('vin') or request.POST.get('vin')  # ✅ Handles form POST too!
        if not vin:
            return Response({"error": "VIN is required"}, status=400)

        url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/{vin}?format=json"
        response = requests.get(url)
        data = response.json()

        make = next((item['Value'] for item in data['Results'] if item['Variable'] == 'Make'), None)
        model = next((item['Value'] for item in data['Results'] if item['Variable'] == 'Model'), None)
        year = next((item['Value'] for item in data['Results'] if item['Variable'] == 'Model Year'), None)

        html_result = f"""
            <html>
            <body>
                <h2>VIN Decode Result</h2>
                <p><strong>VIN:</strong> {vin}</p>
                <p><strong>Make:</strong> {make}</p>
                <p><strong>Model:</strong> {model}</p>
                <p><strong>Year:</strong> {year}</p>
                <a href="/decode-vin">Decode another VIN</a>
            </body>
            </html>
        """
        return HttpResponse(html_result)