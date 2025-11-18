#!/usr/bin/env python3
"""
Bulk update remaining CRM endpoints with company filtering.
"""

import re
from pathlib import Path

CRM_FILE = Path("backend/app/api/v1/endpoints/crm.py")

# Read the file
content = CRM_FILE.read_text()

# Define replacements for deal-related endpoints (need to verify parent deal ownership)
deal_related_updates = [
    # transition_deal_stage
    (
        r'(@router\.post\("/api/deals/\{deal_id\}/transition"\)\s+async def transition_deal_stage\(\s+deal_id: UUID,\s+target_stage: DealStage,\s+force: bool = False,\s+db: Session = Depends\(get_db\))',
        r'\1'  # Keep as is, will manually update
    ),
]

# Automation rules endpoints - these are company-level resources
automation_rules_pattern = r'(@router\.(get|post|put|delete)\("/api/automation/rules.*?"\)\s+async def (get_automation_rules|create_automation_rule|update_automation_rule|delete_automation_rule)\([^)]*db: Session = Depends\(get_db\))'

# First, let's manually construct the updates for automation rules endpoints
print("Automation Rules Endpoints Updates:")
print("=" * 70)

# get_automation_rules
get_automation_rules_old = '''@router.get("/api/automation/rules")
async def get_automation_rules(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Get all automation rules."""
    rules = db.query(DealStageRule).order_by(DealStageRule.priority.desc()).all()
    return {
        "total": len(rules),
        "rules": [rule.to_dict() for rule in rules]
    }'''

get_automation_rules_new = '''@router.get("/api/automation/rules")
async def get_automation_rules(
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get all automation rules."""
    current_user, company = user_company

    query = db.query(DealStageRule)

    # Filter by company_id if user has a company
    if company:
        query = query.filter(DealStageRule.company_id == company.id)

    rules = query.order_by(DealStageRule.priority.desc()).all()
    return {
        "total": len(rules),
        "rules": [rule.to_dict() for rule in rules]
    }'''

# create_automation_rule
create_automation_rule_old = '''@router.post("/api/automation/rules")
async def create_automation_rule(rule_data: Dict[str, Any], db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Create a new automation rule."""
    rule = DealStageRule(**rule_data)
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return {"success": True, "rule": rule.to_dict()}'''

create_automation_rule_new = '''@router.post("/api/automation/rules")
async def create_automation_rule(
    rule_data: Dict[str, Any],
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Create a new automation rule."""
    current_user, company = user_company

    rule = DealStageRule(
        **rule_data,
        company_id=company.id if company else None
    )
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return {"success": True, "rule": rule.to_dict()}'''

# update_automation_rule
update_automation_rule_old = '''@router.put("/api/automation/rules/{rule_id}")
async def update_automation_rule(rule_id: UUID, rule_data: Dict[str, Any], db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Update an automation rule."""
    rule = db.query(DealStageRule).filter(DealStageRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")

    for field, value in rule_data.items():
        setattr(rule, field, value)

    db.commit()
    db.refresh(rule)
    return {"success": True, "rule": rule.to_dict()}'''

update_automation_rule_new = '''@router.put("/api/automation/rules/{rule_id}")
async def update_automation_rule(
    rule_id: UUID,
    rule_data: Dict[str, Any],
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Update an automation rule."""
    current_user, company = user_company

    filters = [DealStageRule.id == rule_id]

    if company:
        filters.append(DealStageRule.company_id == company.id)

    rule = db.query(DealStageRule).filter(*filters).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")

    for field, value in rule_data.items():
        setattr(rule, field, value)

    db.commit()
    db.refresh(rule)
    return {"success": True, "rule": rule.to_dict()}'''

# delete_automation_rule
delete_automation_rule_old = '''@router.delete("/api/automation/rules/{rule_id}")
async def delete_automation_rule(rule_id: UUID, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Delete an automation rule."""
    rule = db.query(DealStageRule).filter(DealStageRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")

    db.delete(rule)
    db.commit()
    return {"success": True, "message": "Rule deleted"}'''

delete_automation_rule_new = '''@router.delete("/api/automation/rules/{rule_id}")
async def delete_automation_rule(
    rule_id: UUID,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Delete an automation rule."""
    current_user, company = user_company

    filters = [DealStageRule.id == rule_id]

    if company:
        filters.append(DealStageRule.company_id == company.id)

    rule = db.query(DealStageRule).filter(*filters).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")

    db.delete(rule)
    db.commit()
    return {"success": True, "message": "Rule deleted"}'''

# Apply updates
updates = [
    (get_automation_rules_old, get_automation_rules_new),
    (create_automation_rule_old, create_automation_rule_new),
    (update_automation_rule_old, update_automation_rule_new),
    (delete_automation_rule_old, delete_automation_rule_new),
]

for old, new in updates:
    if old in content:
        content = content.replace(old, new)
        print(f"✓ Updated endpoint")
    else:
        print(f"✗ Pattern not found")

# Write back
CRM_FILE.write_text(content)

print("\n✓ Automation rules endpoints updated!")
print("\nRemaining endpoints to update manually:")
print("- transition_deal_stage")
print("- check_transition_eligibility")
print("- create_due_diligence_checklist")
print("- pull_comps_for_deal")
print("- get_email_templates")
print("- create_email_template")
print("- Due diligence endpoints (4)")
