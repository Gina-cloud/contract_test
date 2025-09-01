"""Law document processor for external rules."""
import os
import re
from pathlib import Path
from docx import Document

class LawProcessor:
    """Process law documents and extract contract-related rules."""
    
    def __init__(self, laws_dir="laws"):
        self.laws_dir = Path(laws_dir)
        self.raw_docs_dir = self.laws_dir / "raw_docs"
        self.extracted_dir = self.laws_dir / "extracted_text"
        self.rules_dir = self.laws_dir / "processed_rules"
    
    def extract_text_from_docx(self, file_path):
        """Extract text from DOCX file."""
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            print(f"Error extracting from {file_path}: {e}")
            return ""
    
    def process_law_file(self, file_path):
        """Process single law file and extract contract-related content."""
        file_name = Path(file_path).stem
        
        # Extract text
        text = self.extract_text_from_docx(file_path)
        if not text:
            return None
        
        # Save extracted text
        text_file = self.extracted_dir / f"{file_name}.txt"
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(text)
        
        # Extract contract-related sections
        contract_sections = self.extract_contract_sections(text, file_name)
        
        # Save processed rules
        if contract_sections:
            rules_file = self.rules_dir / f"{file_name}_rules.json"
            self.save_rules(contract_sections, rules_file, file_name)
        
        return contract_sections
    
    def extract_contract_sections(self, text, law_name):
        """Extract contract-related sections from law text."""
        contract_keywords = [
            "계약", "용역", "도급", "위탁", "수급", "발주", "공급",
            "대금", "지급", "납기", "검수", "인수", "손해배상",
            "지연", "이자", "위약금", "해지", "해제", "변경"
        ]
        
        sections = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Check if line contains contract-related keywords
            if any(keyword in line for keyword in contract_keywords):
                # Extract article number if present
                article_match = re.search(r'제(\d+)조', line)
                article_num = article_match.group(1) if article_match else None
                
                # Get context (current line + next few lines)
                context_lines = []
                for j in range(i, min(i + 3, len(lines))):
                    if lines[j].strip():
                        context_lines.append(lines[j].strip())
                
                context = ' '.join(context_lines)
                
                sections.append({
                    "law_name": law_name,
                    "article": article_num,
                    "content": line,
                    "context": context,
                    "keywords": [kw for kw in contract_keywords if kw in line]
                })
        
        return sections
    
    def save_rules(self, sections, file_path, law_name):
        """Save extracted rules to JSON file."""
        import json
        
        rules = {
            "law_name": law_name,
            "version": "2.0",
            "sections": sections
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(rules, f, ensure_ascii=False, indent=2)
    
    def process_all_files(self):
        """Process all DOC/DOCX files in raw_docs directory."""
        doc_files = list(self.raw_docs_dir.glob("*.doc*"))
        
        if not doc_files:
            print("No DOC/DOCX files found in laws/raw_docs/")
            print("Please upload your law documents to laws/raw_docs/ directory")
            return []
        
        results = []
        for file_path in doc_files:
            print(f"Processing: {file_path.name}")
            sections = self.process_law_file(file_path)
            if sections:
                results.append({
                    "file": file_path.name,
                    "sections_count": len(sections)
                })
        
        return results

if __name__ == "__main__":
    processor = LawProcessor()
    results = processor.process_all_files()
    
    print(f"\nProcessed {len(results)} law files:")
    for result in results:
        print(f"- {result['file']}: {result['sections_count']} contract-related sections")