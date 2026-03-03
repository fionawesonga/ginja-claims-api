from django.test import TestCase
from decimal import Decimal
from claims.models import Member, ProcedureCost, Claim
from fraud.models import ClaimValidation
from fraud.services import run_claim_validation

class ClaimValidationModelTest(TestCase):
    def setUp(self):
        self.member = Member.objects.create(
            member_id="M999", first_name="Test", last_name="User",
            eligibility_status="active", enrollment_date="2025-01-01"
        )
        self.procedure = ProcedureCost.objects.create(
            procedure_code="P999", procedure_name="Testing Procedure",
            average_cost=Decimal("1000.00")
        )
        self.claim = Claim.objects.create(
            claim_id="C999", member=self.member, provider_id="H999",
            diagnosis_code="D999", procedure=self.procedure,
            claim_amount=Decimal("500.00")
        )
        self.validation = ClaimValidation.objects.create(
            claim=self.claim, eligibility_check=True, benefit_limit_ok=True,
            fraud_flag=False, approved_amount=Decimal("500.00"), status="APPROVED"
        )

    def test_validation_creation(self):
        val = ClaimValidation.objects.get(validation_id=self.validation.validation_id)
        self.assertEqual(val.claim.claim_id, "C999")

class ValidationLogicTest(TestCase):
    def setUp(self):
        self.member_active = Member.objects.create(
            member_id="M_ACTIVE", first_name="Active", last_name="User",
            eligibility_status="active", enrollment_date="2025-01-01"
        )
        self.member_inactive = Member.objects.create(
            member_id="M_INACTIVE", first_name="Inactive", last_name="User",
            eligibility_status="inactive", enrollment_date="2025-01-01"
        )
        self.procedure = ProcedureCost.objects.create(
            procedure_code="P_TEST", procedure_name="Test Proc",
            average_cost=Decimal("10000.00")
        )

    def test_logic_approved(self):
        claim = Claim.objects.create(
            claim_id="C_APPROVE", member=self.member_active, provider_id="H1",
            diagnosis_code="D1", procedure=self.procedure, claim_amount=Decimal("5000.00")
        )
        result = run_claim_validation(claim)
        self.assertEqual(result.status, "APPROVED")

    def test_logic_fraud_rejection(self):
        claim = Claim.objects.create(
            claim_id="C_FRAUD", member=self.member_active, provider_id="H1",
            diagnosis_code="D1", procedure=self.procedure, claim_amount=Decimal("25000.00")
        )
        result = run_claim_validation(claim)
        self.assertEqual(result.status, "REJECTED")
        self.assertTrue(result.fraud_flag)

    def test_logic_partial_approval(self):
        claim = Claim.objects.create(
            claim_id="C_PARTIAL", member=self.member_active, provider_id="H1",
            diagnosis_code="D1", procedure=self.procedure, claim_amount=Decimal("50000.00")
        )
        result = run_claim_validation(claim)
        self.assertEqual(result.status, "PARTIAL")
