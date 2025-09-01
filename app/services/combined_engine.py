"""Combined rules engine: Internal + Legal rules."""
from app.services.rules_engine import RulesEngine
from app.services.smart_law_engine import SmartLawEngine
from app.models.schema import AuditResult

class CombinedRulesEngine:
    """Combined engine for internal rules + legal compliance."""
    
    def __init__(self, internal_rules_file="rules/base.rules.json"):
        self.internal_engine = RulesEngine(internal_rules_file)
        self.law_engine = SmartLawEngine()
    
    def evaluate_contract(self, contract_text):
        """Evaluate contract with both internal and legal rules."""
        
        # Step 1: Internal rules check
        internal_result = self.internal_engine.evaluate_contract(contract_text)
        
        # Step 2: Smart legal compliance check
        legal_result, contract_type = self.law_engine.evaluate_contract(contract_text)
        
        # Store contract type for UI display
        self.detected_contract_type = contract_type
        
        # Combine results
        all_violations = internal_result.rule_results + legal_result.rule_results
        
        # Count total violations
        total_required = sum(1 for v in all_violations if v.severity == "required")
        total_recommended = sum(1 for v in all_violations if v.severity == "recommended")
        
        return AuditResult(
            total_rules=len(all_violations),
            required_violations=total_required,
            recommended_violations=total_recommended,
            rule_results=all_violations
        )