"""Setup script for 2차_외부규칙포함 version."""
import os
import shutil

def setup_phase2():
    """Setup directory structure for phase 2."""
    
    # Create laws directory
    laws_dir = "laws"
    if not os.path.exists(laws_dir):
        os.makedirs(laws_dir)
        print(f"Created {laws_dir}/ directory")
    
    # Create subdirectories
    subdirs = ["raw_docs", "extracted_text", "processed_rules"]
    for subdir in subdirs:
        path = os.path.join(laws_dir, subdir)
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Created {laws_dir}/{subdir}/ directory")
    
    print("\n📁 Directory structure created:")
    print("laws/")
    print("├── raw_docs/          # 28개 법률 워드파일 업로드")
    print("├── extracted_text/    # 추출된 텍스트 파일")
    print("└── processed_rules/   # 변환된 규칙 파일")
    print("\n✅ Ready for 2차_외부규칙포함 development!")

if __name__ == "__main__":
    setup_phase2()