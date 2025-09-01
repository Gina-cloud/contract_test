"""Smart law engine that applies relevant laws only."""
import json
from pathlib import Path
from app.models.schema import RuleResult, AuditResult

class SmartLawEngine:
    """Apply only relevant laws based on contract type."""
    
    def __init__(self, laws_dir="laws/processed_rules"):
        self.laws_dir = Path(laws_dir)
        self.law_rules = self.load_all_law_rules()
        
        # Define law relevance mapping
        self.law_relevance = {
            "용역계약": ["민법", "상법", "소프트웨어 진흥법", "하도급거래"],
            "개발계약": ["민법", "상법", "소프트웨어 진흥법", "정보통신"],
            "공급계약": ["민법", "상법", "하도급거래"],
            "일반계약": ["민법", "상법"]
        }
    
    def load_all_law_rules(self):
        """Load all law rules."""
        rules = {}
        for rule_file in self.laws_dir.glob("*_rules.json"):
            try:
                with open(rule_file, 'r', encoding='utf-8') as f:
                    law_data = json.load(f)
                    law_name = law_data.get('law_name', rule_file.stem)
                    rules[law_name] = law_data['sections']
            except:
                continue
        return rules
    
    def detect_contract_type(self, contract_text):
        """Detect contract type from text."""
        text_lower = contract_text.lower()
        
        if any(word in text_lower for word in ['용역', '서비스', '개발', '소프트웨어']):
            if any(word in text_lower for word in ['개발', '소프트웨어', '시스템']):
                return "개발계약"
            return "용역계약"
        elif any(word in text_lower for word in ['공급', '납품', '제품']):
            return "공급계약"
        else:
            return "일반계약"
    
    def get_relevant_laws(self, contract_type):
        """Get laws relevant to contract type."""
        relevant_keywords = self.law_relevance.get(contract_type, ["민법", "상법"])
        
        relevant_laws = {}
        for law_name, sections in self.law_rules.items():
            # Check if law is relevant
            if any(keyword in law_name for keyword in relevant_keywords):
                relevant_laws[law_name] = sections
        
        return relevant_laws
    
    def evaluate_contract(self, contract_text):
        """Evaluate contract with relevant laws only."""
        # Detect contract type
        contract_type = self.detect_contract_type(contract_text)
        
        # Get relevant laws
        relevant_laws = self.get_relevant_laws(contract_type)
        
        violations = []
        
        # Check only relevant laws
        for law_name, sections in relevant_laws.items():
            # Simple check for demonstration
            if "민법" in law_name and "손해배상" not in contract_text:
                violations.append(RuleResult(
                    rule_id=f"LAW-민법-750",
                    title="민법 제750조 손해배상 책임",
                    severity="recommended",
                    status="missing",
                    suggestion="[법률 검토] 민법 제750조에 따른 손해배상 조항을 검토하시기 바랍니다.",
                    evidence="",
                    law_reference="민법 제750조"
                ))
            
            if "상법" in law_name and "계약" in contract_text:
                violations.append(RuleResult(
                    rule_id=f"LAW-상법-527",
                    title="상법 계약 관련 조항",
                    severity="recommended",
                    status="present",
                    suggestion="[법률 확인] 상법상 계약 조항이 적절히 반영되어 있습니다.",
                    evidence="",
                    law_reference="상법 관련 조항"
                ))
        
        # Count violations
        required_violations = sum(1 for v in violations if v.severity == "required")
        recommended_violations = sum(1 for v in violations if v.severity == "recommended")
        
        return AuditResult(
            total_rules=len(violations),
            required_violations=required_violations,
            recommended_violations=recommended_violations,
            rule_results=violations
        ), contract_type