import uuid
import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from claims.models import Claim, Member, ProcedureCost
from fraud.models import ClaimValidation
from fraud.services import run_claim_validation
from .serializers import ClaimInputSerializer

logger = logging.getLogger(__name__)

class ClaimViewSet(viewsets.ViewSet):
    """ViewSet for handling claim submission and status retrieval."""
    
    def create(self, request):
        """Submit a new claim (POST /api/claims/)"""
        serializer = ClaimInputSerializer(data=request.data)
        
        if serializer.is_valid():
            data = serializer.validated_data
            
            try:
                member = Member.objects.get(member_id=data['member_id'])
            except Member.DoesNotExist:
                return Response({"error": "Member not found"}, status=status.HTTP_404_NOT_FOUND)

            try:
                procedure = ProcedureCost.objects.get(procedure_code=data['procedure_code'])
            except ProcedureCost.DoesNotExist:
                return Response({"error": "Invalid Procedure Code"}, status=status.HTTP_400_BAD_REQUEST)

            claim_id = f"C{uuid.uuid4().hex[:6].upper()}"
            
            claim = Claim.objects.create(
                claim_id=claim_id,
                member=member,
                provider_id=data['provider_id'],
                diagnosis_code=data['diagnosis_code'],
                procedure=procedure,
                claim_amount=data['claim_amount']
            )

            validation_result = run_claim_validation(claim)

            return Response({
                "claim_id": claim.claim_id,
                "status": validation_result.status,
                "fraud_flag": validation_result.fraud_flag,
                "approved_amount": str(validation_result.approved_amount)
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Retrieve claim status by claim_id (GET /api/claims/{claim_id}/)"""
        try:
            claim = Claim.objects.get(claim_id=pk)
            validation = claim.claimvalidation
            
            return Response({
                "claim_id": claim.claim_id,
                "status": validation.status,
                "fraud_flag": validation.fraud_flag,
                "approved_amount": str(validation.approved_amount)
            }, status=status.HTTP_200_OK)
            
        except Claim.DoesNotExist:
            return Response({"error": "Claim not found"}, status=status.HTTP_404_NOT_FOUND)
        except ClaimValidation.DoesNotExist:
            return Response({"error": "Validation data missing"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """List all claims (GET /api/claims/)"""
        claims = Claim.objects.all().order_by('-claim_date')
        data = [
            {
                "claim_id": c.claim_id,
                "member_id": c.member.member_id,
                "procedure_code": c.procedure.procedure_code,
                "claim_amount": str(c.claim_amount),
                "claim_date": str(c.claim_date)
            }
            for c in claims
        ]
        return Response({"claims": data})
