"""Extract text from single law file for testing."""
import subprocess
import os

def extract_with_antiword(doc_path):
    """Try to extract text using antiword if available."""
    try:
        result = subprocess.run(['antiword', doc_path], 
                              capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            return result.stdout
    except:
        pass
    return None

def extract_민법():
    """Extract text from 민법 file."""
    doc_path = "laws/raw_docs/민법(법률)(제20432호)(20250131).doc"
    
    if not os.path.exists(doc_path):
        print(f"File not found: {doc_path}")
        return
    
    # Try antiword first
    text = extract_with_antiword(doc_path)
    
    if text:
        # Save extracted text
        with open("laws/extracted_text/민법.txt", "w", encoding="utf-8") as f:
            f.write(text)
        
        print(f"민법 텍스트 추출 완료: {len(text):,} 문자")
        
        # Show sample
        lines = text.split('\n')[:20]
        print("\n=== 민법 샘플 텍스트 ===")
        for line in lines:
            if line.strip():
                print(line.strip())
        
        return text
    else:
        print("텍스트 추출 실패. 수동으로 DOCX 변환이 필요합니다.")
        print("Word에서 민법.doc을 열어 DOCX로 저장해주세요.")
        return None

if __name__ == "__main__":
    extract_민법()