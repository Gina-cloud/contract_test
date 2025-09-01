"""Rules engine for contract evaluation."""
import json
import re
from typing import List, Dict, Any
from app.models.schema import RuleResult, AuditResult


class RulesEngine:
    def __init__(self, rules_file_path: str):
        with open(rules_file_path, 'r', encoding='utf-8') as f:
            self.rules_data = json.load(f)
        self.rules = self.rules_data['rules']
        self.params = self.rules_data.get('params', {})
    
    def evaluate_contract(self, text: str) -> AuditResult:
        """Evaluate contract text against all rules."""
        rule_results = []
        required_violations = 0
        recommended_violations = 0
        
        for rule in self.rules:
            result = self._evaluate_rule(rule, text)
            rule_results.append(result)
            
            if result.status != "present":
                if result.severity == "required":
                    required_violations += 1
                else:
                    recommended_violations += 1
        
        return AuditResult(
            total_rules=len(self.rules),
            required_violations=required_violations,
            recommended_violations=recommended_violations,
            rule_results=rule_results
        )
    
    def _evaluate_rule(self, rule: Dict[str, Any], text: str) -> RuleResult:
        """Evaluate a single rule against text."""
        text_lower = text.lower()
        
        # Check if detect keywords are present
        detect_found = any(keyword.lower() in text_lower for keyword in rule['detect'])
        
        if not detect_found:
            return RuleResult(
                rule_id=rule['id'],
                title=rule['title'],
                severity=rule['severity'],
                status="missing",
                suggestion=rule['suggestion'],
                redline_action="add"
            )
        
        # Find evidence snippet
        evidence = self._find_evidence(text, rule['detect'])
        
        # Check must_include conditions
        if 'must_include_all' in rule:
            all_present = all(req.lower() in text_lower for req in rule['must_include_all'])
            status = "present" if all_present else "insufficient"
        elif 'must_include' in rule:
            all_present = all(req.lower() in text_lower for req in rule['must_include'])
            status = "present" if all_present else "insufficient"
        elif 'must_include_any' in rule:
            any_present = any(req.lower() in text_lower for req in rule['must_include_any'])
            status = "present" if any_present else "insufficient"
        else:
            status = "present"  # Only detect keywords required
        
        return RuleResult(
            rule_id=rule['id'],
            title=rule['title'],
            severity=rule['severity'],
            status=status,
            evidence=evidence,
            suggestion=rule['suggestion'],
            redline_action="replace" if status == "insufficient" else None
        )
    
    def _find_evidence(self, text: str, detect_keywords: List[str]) -> str:
        """Find evidence snippet around detect keywords (±40 chars)."""
        text_lower = text.lower()
        
        for keyword in detect_keywords:
            keyword_lower = keyword.lower()
            pos = text_lower.find(keyword_lower)
            if pos != -1:
                start = max(0, pos - 40)
                end = min(len(text), pos + len(keyword) + 40)
                return f"...{text[start:end]}..."
        
        return None