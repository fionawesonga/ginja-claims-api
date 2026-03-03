from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from claims.models import Member, ProcedureCost, Claim
from fraud.models import ClaimValidation
from decimal import Decimal

class ClaimAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.member = Member.objects.create(
            member_id="M_API", first_name="Api", last_name="Tester",
            eligibility_status="active", enrollment_date="2025-01-01"
        )
        self.procedure = ProcedureCost.objects.create(
            procedure_code="P_API", procedure_name="API Test Procedure",
            average_cost=Decimal("10000.00")
        )
        self.valid_payload = {
            "member_id": "M_API", "provider_id": "H_PROVIDER",
            "diagnosis_code": "D_API", "procedure_code": "P_API",
            "claim_amount": 5000.00
        }

    def test_submit_claim_success(self):
        response = self.client.post('/claims', self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'APPROVED')

    def test_retrieve_claim_status(self):
        claim = Claim.objects.create(
            claim_id="C_GET_TEST", member=self.member, provider_id="H_GET",
            diagnosis_code="D_GET", procedure=self.procedure, claim_amount=Decimal("1000.00")
        )
        ClaimValidation.objects.create(
            claim=claim, eligibility_check=True, benefit_limit_ok=True,
            fraud_flag=False, approved_amount=Decimal("1000.00"), status="APPROVED"
        )
        response = self.client.get('/claims/C_GET_TEST')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], "APPROVED")
