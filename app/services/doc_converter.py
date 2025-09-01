"""DOC file converter using win32com."""
import os
import win32com.client
from pathlib import Path

class DocConverter:
    """Convert DOC files to text using Word COM interface."""
    
    def __init__(self):
        self.word_app = None
    
    def start_word(self):
        """Start Word application."""
        try:
            self.word_app = win32com.client.Dispatch("Word.Application")
            self.word_app.Visible = False
            return True
        except Exception as e:
            print(f"Failed to start Word: {e}")
            return False
    
    def close_word(self):
        """Close Word application."""
        if self.word_app:
            self.word_app.Quit()
            self.word_app = None
    
    def convert_doc_to_text(self, doc_path):
        """Convert DOC file to text."""
        if not self.word_app:
            if not self.start_word():
                return ""
        
        try:
            # Open document
            doc = self.word_app.Documents.Open(str(doc_path))
            
            # Extract text
            text = doc.Content.Text
            
            # Close document
            doc.Close(False)
            
            return text
        except Exception as e:
            print(f"Error converting {doc_path}: {e}")
            return ""
    
    def convert_all_docs(self, input_dir, output_dir):
        """Convert all DOC files in directory to text files."""
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        
        doc_files = list(input_path.glob("*.doc"))
        
        if not doc_files:
            print("No DOC files found")
            return []
        
        if not self.start_word():
            return []
        
        results = []
        
        try:
            for doc_file in doc_files:
                print(f"Converting: {doc_file.name}")
                
                text = self.convert_doc_to_text(doc_file)
                
                if text:
                    # Save as text file
                    text_file = output_path / f"{doc_file.stem}.txt"
                    with open(text_file, 'w', encoding='utf-8') as f:
                        f.write(text)
                    
                    results.append({
                        "file": doc_file.name,
                        "text_length": len(text),
                        "output": text_file.name
                    })
        
        finally:
            self.close_word()
        
        return results

if __name__ == "__main__":
    converter = DocConverter()
    results = converter.convert_all_docs("laws/raw_docs", "laws/extracted_text")
    
    print(f"\nConverted {len(results)} files:")
    for result in results:
        print(f"- {result['file']} -> {result['output']} ({result['text_length']:,} chars)")