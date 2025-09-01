"""Main entry point for Streamlit Cloud deployment."""
import sys
from pathlib import Path

# Add current directory to Python path
sys.path.append(str(Path(__file__).parent))

# Import and run the main app
from ui.streamlit_app import main

if __name__ == "__main__":
    main()