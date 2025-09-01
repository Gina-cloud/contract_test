"""Integration test for the complete workflow."""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from app.services.extractor import extract_text_from_docx
from app.services.rules_engine import RulesEngine
from app.services.redline_docx import RedlineGenerator


def test_complete_workflow():
    """Test the complete workflow with sample document."""
    print("[INFO] Starting integration test...")
    
    # 1. Load sample document
    with open("sample_docs/sample1.docx", "rb") as f:
        file_bytes = f.read()
    
    # 2. Extract text
    text = extract_text_from_docx(file_bytes)
    print(f"[OK] Text extracted: {len(text)} characters")
    
    # 3. Evaluate rules
    engine = RulesEngine("rules/base.rules.json")
    audit_result = engine.evaluate_contract(text)
    print(f"[OK] Rules evaluated: {audit_result.total_rules} rules")
    print(f"[INFO] Required violations: {audit_result.required_violations}")
    print(f"[INFO] Recommended violations: {audit_result.recommended_violations}")
    
    # 4. Generate redline
    generator = RedlineGenerator()
    redline_bytes = generator.generate_redline_docx(file_bytes, audit_result)
    
    # 5. Save redline output
    with open("integration_test_output.docx", "wb") as f:
        f.write(redline_bytes)
    
    print("[OK] Redline DOCX generated")
    print("[SUCCESS] Integration test completed!")
    print("[INFO] Output saved to: integration_test_output.docx")
    
    return audit_result


if __name__ == "__main__":
    result = test_complete_workflow()
    
    # Print detailed results
    print("\n=== DETAILED RESULTS ===")
    for rule_result in result.rule_results:
        status_symbol = {"present": "[OK]", "insufficient": "[WARN]", "missing": "[ERROR]"}[rule_result.status]
        print(f"{status_symbol} {rule_result.rule_id}: {rule_result.title} - {rule_result.status}")
        if rule_result.evidence:
            print(f"    Evidence: {rule_result.evidence}")
        if rule_result.status != "present":
            print(f"    Suggestion: {rule_result.suggestion}")
        print()