from django.db import models
from claims.models import Claim

class ClaimValidation(models.Model):
    STATUS_CHOICES = [
        ('APPROVED', 'Approved'),
        ('PARTIAL', 'Partial'),
        ('REJECTED', 'Rejected'),
    ]

    validation_id = models.AutoField(primary_key=True)
    claim = models.OneToOneField(Claim, on_delete=models.CASCADE)
    eligibility_check = models.BooleanField(default=False)
    benefit_limit_ok = models.BooleanField(default=False)
    fraud_flag = models.BooleanField(default=False)
    approved_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='REJECTED')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Validation for {self.claim.claim_id}"
