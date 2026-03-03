from django.test import TestCase
from decimal import Decimal
from claims.models import Member, ProcedureCost, Claim
from datetime import date

class MemberModelTest(TestCase):
    def setUp(self):
        self.member = Member.objects.create(
            member_id="M001", first_name="John", last_name="Doe",
            eligibility_status="active", enrollment_date="2025-01-01"
        )

    def test_member_creation(self):
        member = Member.objects.get(member_id="M001")
        self.assertEqual(member.first_name, "John")
        self.assertEqual(member.eligibility_status, "active")

    def test_member_str_representation(self):
        self.assertEqual(str(self.member), "M001 - John")

class ProcedureCostModelTest(TestCase):
    def setUp(self):
        self.procedure = ProcedureCost.objects.create(
            procedure_code="P001", procedure_name="General Checkup",
            average_cost=Decimal("1500.00")
        )

    def test_procedure_creation(self):
        proc = ProcedureCost.objects.get(procedure_code="P001")
        self.assertEqual(proc.procedure_name, "General Checkup")
        self.assertEqual(proc.average_cost, Decimal("1500.00"))

    def test_procedure_str_representation(self):
        self.assertEqual(str(self.procedure), "P001")

class ClaimModelTest(TestCase):
    def setUp(self):
        self.member = Member.objects.create(
            member_id="M002", first_name="Jane", last_name="Doe",
            eligibility_status="active", enrollment_date="2025-01-01"
        )
        self.procedure = ProcedureCost.objects.create(
            procedure_code="P002", procedure_name="Surgery",
            average_cost=Decimal("5000.00")
        )
        self.claim = Claim.objects.create(
            claim_id="C001", member=self.member, provider_id="H123",
            diagnosis_code="D001", procedure=self.procedure,
            claim_amount=Decimal("4500.00")
        )

    def test_claim_creation(self):
        claim = Claim.objects.get(claim_id="C001")
        self.assertEqual(claim.member.first_name, "Jane")
        self.assertEqual(claim.procedure.procedure_name, "Surgery")
        self.assertEqual(claim.claim_amount, Decimal("4500.00"))

    def test_claim_auto_date(self):
        claim = Claim.objects.get(claim_id="C001")
        self.assertEqual(claim.claim_date, date.today())

    def test_claim_str_representation(self):
        self.assertEqual(str(self.claim), "C001")
