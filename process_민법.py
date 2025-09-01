"""Process 민법 and extract contract-related rules."""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from app.services.law_processor import LawProcessor
import json

def process_민법():
    """Process 민법 sample text."""
    
    # Read sample text
    with open("laws/extracted_text/민법_샘플.txt", "r", encoding="utf-8") as f:
        text = f.read()
    
    print(f"민법 텍스트 길이: {len(text):,} 문자")
    
    # Extract contract-related sections
    processor = LawProcessor()
    sections = processor.extract_contract_sections(text, "민법")
    
    print(f"\n계약 관련 조항 {len(sections)}개 추출:")
    
    # Show extracted sections
    for i, section in enumerate(sections, 1):
        print(f"\n{i}. 제{section['article']}조: {section['content'][:100]}...")
        print(f"   키워드: {', '.join(section['keywords'])}")
    
    # Save as rules
    if sections:
        rules_file = "laws/processed_rules/민법_rules.json"
        processor.save_rules(sections, rules_file, "민법")
        print(f"\n규칙 파일 저장: {rules_file}")
    
    return sections

if __name__ == "__main__":
    sections = process_민법()