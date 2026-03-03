from django.db import models

class Member(models.Model):
    member_id = models.CharField(max_length=50, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    eligibility_status = models.CharField(
        max_length=20, 
        choices=[('active', 'Active'), ('inactive', 'Inactive')]
    )
    enrollment_date = models.DateField()

    def __str__(self):
        return f"{self.member_id} - {self.first_name}"

class ProcedureCost(models.Model):
    procedure_code = models.CharField(max_length=50, primary_key=True)
    procedure_name = models.CharField(max_length=100)
    average_cost = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.procedure_code

class Claim(models.Model):
    claim_id = models.CharField(max_length=50, primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    provider_id = models.CharField(max_length=50)
    diagnosis_code = models.CharField(max_length=50)
    procedure = models.ForeignKey(ProcedureCost, on_delete=models.CASCADE)
    claim_amount = models.DecimalField(max_digits=12, decimal_places=2)
    claim_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.claim_id
