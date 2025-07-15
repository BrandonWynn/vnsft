# core/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import PingSerializer, VehicleSerializer, ServiceSerializer
from .models import Vehicle, Service
import logging
import json
import requests
from django.http import HttpResponse

logger = logging.getLogger(__name__)


class PingView(APIView):
    """
    GET /ping/  → returns {"message": "pong"}
    """
    permission_classes = [AllowAny]

    def get(self, request):
        serializer = PingSerializer({"message": "pong"})
        return Response(serializer.data, status=status.HTTP_200_OK)


class CallbackView(APIView):
    """
    GET /callback/ → Handles Manheim OAuth redirect
    POST /callback/ → Handles Manheim webhooks
    """
    permission_classes = [AllowAny]

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        code = request.query_params.get('code')
        error = request.query_params.get('error')
        if error:
            logger.error(f"Manheim API error: {error}")
            return Response({"error": f"Manheim choked: {error}"}, status=status.HTTP_400_BAD_REQUEST)
        logger.info(f"Got OAuth code: {code}")
        return Response({"message": "OAuth callback received!"}, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            data = request.data
            logger.info(f"Webhook data: {data}")
            return Response({"message": "Webhook received."}, status=status.HTTP_200_OK)
        except json.JSONDecodeError:
            logger.error("Invalid webhook JSON")
            return Response({"error": "Bad JSON"}, status=status.HTTP_400_BAD_REQUEST)


class DecodeVinView(APIView):
    """
    GET → Browser HTML test form
    POST → Calls NHTSA to decode VIN and display result in HTML
    """
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
        vin = request.data.get('vin') or request.POST.get('vin')
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


class VehicleListCreateView(APIView):
    """
    GET: List vehicles for user's assigned locations
    POST: Add vehicle with AS400 + NHTSA VIN match
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        locations = request.user.assigned_locations.all()
        vehicles = Vehicle.objects.filter(location__in=locations)
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        vin = request.data.get('vin')
        location_id = request.data.get('location')

        if not vin:
            return Response({"error": "VIN is required"}, status=400)

        # Example AS400 data (replace with real call)
        as400_data = {
            "year": "2025",
            "make": "Ford",
            "model": "F-150",
            "account_name": "Big Auction",
            "work_order": "WO123456",
        }

        nhtsa_url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/{vin}?format=json"
        nhtsa_response = requests.get(nhtsa_url, timeout=10)
        nhtsa_data = nhtsa_response.json()
        nhtsa_year = next((i['Value'] for i in nhtsa_data['Results'] if i['Variable'] == 'Model Year'), None)

        if nhtsa_year and nhtsa_year != as400_data["year"]:
            logger.warning(f"VIN mismatch: AS400 year {as400_data['year']}, NHTSA year {nhtsa_year}")
            return Response({"error": "VIN year mismatch. Manual check needed."}, status=400)

        vehicle, created = Vehicle.objects.get_or_create(
            vin=vin,
            defaults={
                "year": as400_data["year"],
                "make": as400_data["make"],
                "model": as400_data["model"],
                "account_name": as400_data["account_name"],
                "work_order": as400_data["work_order"],
                "location_id": location_id
            }
        )
        serializer = VehicleSerializer(vehicle)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class ServiceListCreateView(APIView):
    """
    GET: List services for user's assigned locations
    POST: Create new service log
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        locations = request.user.assigned_locations.all()
        services = Service.objects.filter(vehicle__location__in=locations)
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(started_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
