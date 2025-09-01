"""Law-based rules engine for external legal compliance."""
import json
import os
from pathlib import Path
from app.models.schema import RuleResult, AuditResult

class LawRulesEngine:
    """Engine for checking contracts against legal requirements."""
    
    def __init__(self, laws_dir="laws/processed_rules"):
        self.laws_dir = Path(laws_dir)
        self.law_rules = self.load_all_law_rules()
    
    def load_all_law_rules(self):
        """Load all processed law rules."""
        rules = {}
        
        if not self.laws_dir.exists():
            return rules
        
        for rule_file in self.laws_dir.glob("*_rules.json"):
            try:
                with open(rule_file, 'r', encoding='utf-8') as f:
                    law_data = json.load(f)
                    law_name = law_data.get('law_name', rule_file.stem)
                    rules[law_name] = law_data['sections']
            except Exception as e:
                print(f"Error loading {rule_file}: {e}")
        
        return rules
    
    def check_contract_against_laws(self, contract_text):
        """Check contract text against all loaded laws."""
        violations = []
        
        for law_name, sections in self.law_rules.items():
            law_violations = self.check_single_law(contract_text, law_name, sections)
            violations.extend(law_violations)
        
        return violations
    
    def check_single_law(self, contract_text, law_name, sections):
        """Check contract against single law."""
        violations = []
        contract_lower = contract_text.lower()
        
        for section in sections:
            # Simple keyword matching for now
            keywords = section.get('keywords', [])
            content = section.get('content', '')
            article = section.get('article', '')
            
            # Check if any keywords are missing or problematic
            for keyword in keywords:
                if keyword in ['계약', '용역', '대금', '지급']:
                    # Check for potential violations
                    violation = self.analyze_section_compliance(
                        contract_text, section, law_name
                    )
                    if violation:
                        violations.append(violation)
                        break  # One violation per section
        
        return violations
    
    def analyze_section_compliance(self, contract_text, section, law_name):
        """Analyze if contract complies with specific law section."""
        content = section.get('content', '')
        article = section.get('article', '')
        keywords = section.get('keywords', [])
        
        # Simple compliance rules
        rule_id = f"LAW-{law_name[:3].upper()}-{article or '000'}"
        
        # Check for common violations
        if '손해배상' in keywords and '손해배상' not in contract_text:
            return RuleResult(
                rule_id=rule_id,
                title=f"{law_name} 제{article}조 손해배상 조항",
                severity="recommended",
                status="missing",
                suggestion=f"[법률 검토] {law_name} 제{article}조에 따른 손해배상 조항을 검토하시기 바랍니다.",
                evidence="",
                law_reference=f"{law_name} 제{article}조"
            )
        
        if '지연' in keywords and '지연' in contract_text and '이자' not in contract_text:
            return RuleResult(
                rule_id=rule_id,
                title=f"{law_name} 제{article}조 지연이자 조항",
                severity="recommended", 
                status="insufficient",
                suggestion=f"[법률 검토] {law_name} 제{article}조에 따른 지연이자 조항을 명시하시기 바랍니다.",
                evidence=content[:100] + "...",
                law_reference=f"{law_name} 제{article}조"
            )
        
        return None
    
    def evaluate_contract(self, contract_text):
        """Evaluate contract against all laws."""
        violations = self.check_contract_against_laws(contract_text)
        
        # Count violations by severity
        required_violations = sum(1 for v in violations if v.severity == "required")
        recommended_violations = sum(1 for v in violations if v.severity == "recommended")
        
        return AuditResult(
            total_rules=len(violations),
            required_violations=required_violations,
            recommended_violations=recommended_violations,
            rule_results=violations
        )