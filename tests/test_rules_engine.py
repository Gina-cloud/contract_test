"""Tests for rules engine."""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from app.services.rules_engine import RulesEngine


def test_pay_001_insufficient():
    """Test PAY-001 rule with insufficient condition."""
    engine = RulesEngine("rules/base.rules.json")
    text = "지연 시 이자를 지급한다."
    
    result = engine.evaluate_contract(text)
    pay_001 = next(r for r in result.rule_results if r.rule_id == "PAY-001")
    
    assert pay_001.status == "insufficient"
    assert "지연" in pay_001.evidence
    print("[OK] PAY-001 insufficient test passed")


def test_acc_005_present():
    """Test ACC-005 rule with present condition."""
    engine = RulesEngine("rules/base.rules.json")
    text = "검수요청일로부터 5영업일 내 결과 통지, 미통지는 합격으로 본다."
    
    result = engine.evaluate_contract(text)
    acc_005 = next(r for r in result.rule_results if r.rule_id == "ACC-005")
    
    assert acc_005.status == "present"
    print("[OK] ACC-005 present test passed")


def test_dam_001_missing():
    """Test DAM-001 rule with missing condition."""
    engine = RulesEngine("rules/base.rules.json")
    text = "손해배상 책임은 무제한으로 한다."
    
    result = engine.evaluate_contract(text)
    dam_001 = next(r for r in result.rule_results if r.rule_id == "DAM-001")
    
    assert dam_001.status == "insufficient"  # detect found but must_include_any not satisfied
    print("[OK] DAM-001 insufficient test passed")


if __name__ == "__main__":
    test_pay_001_insufficient()
    test_acc_005_present()
    test_dam_001_missing()
    print("[SUCCESS] All rules engine tests passed!")