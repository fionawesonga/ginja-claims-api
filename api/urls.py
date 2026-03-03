from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.views import APIView
from rest_framework.response import Response
from .views import ClaimViewSet

router = DefaultRouter()
router.register(r'claims', ClaimViewSet, basename='claim')

class APIRoot(APIView):
    def get(self, request, format=None):
        return Response({
            "message": "Welcome to Ginja AI Claims API",
            "endpoints": {
                "submit_claim": "POST /api/claims/ - Submit new claim",
                "get_claim_status": "GET /api/claims/{claim_id}/ - Get claim status",
                "list_claims": "GET /api/claims/ - List all claims"
            }
        })

urlpatterns = [
    path('', APIRoot.as_view(), name='api-root'),
    path('', include(router.urls)),
]
