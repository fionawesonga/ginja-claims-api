from decimal import Decimal
from fraud.models import ClaimValidation

def run_claim_validation(claim_obj):
    member = claim_obj.member
    procedure = claim_obj.procedure
    claim_amt = claim_obj.claim_amount
    
    # Defaults
    is_eligible = False
    is_benefit_ok = False
    is_fraud = False
    final_status = 'REJECTED'
    approved_amt = Decimal('0.00')
    
    # 1. Eligibility Check
    if member.eligibility_status == 'active':
        is_eligible = True
    
    # 2. Benefit Limit Check (Max 40,000)
    BENEFIT_LIMIT = Decimal('40000.00')
    if claim_amt <= BENEFIT_LIMIT:
        is_benefit_ok = True

    # 3. Fraud Rule
    avg_cost = procedure.average_cost
    if claim_amt > (avg_cost * Decimal('2.0')):
        is_fraud = True

    # 4. Decision Logic
    if not is_eligible:
        final_status = 'REJECTED'
    elif is_fraud:
        final_status = 'REJECTED'
    elif not is_benefit_ok:
        final_status = 'PARTIAL'
        approved_amt = BENEFIT_LIMIT
    else:
        final_status = 'APPROVED'
        approved_amt = claim_amt

    # 5. Save Result
    validation = ClaimValidation.objects.create(
        claim=claim_obj,
        eligibility_check=is_eligible,
        benefit_limit_ok=is_benefit_ok,
        fraud_flag=is_fraud,
        approved_amount=approved_amt,
        status=final_status
    )
    return validation
