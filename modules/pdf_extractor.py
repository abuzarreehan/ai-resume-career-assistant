"""
PDF Text Extraction and Validation Module.
Uses pypdf to extract text cleanly with error handling.
"""
import io
from pypdf import PdfReader

def extract_text_from_pdf(file_bytes: bytes) -> tuple[str, bool, str]:
    """
    Extracts selectable text from an uploaded PDF file byte stream.
    Returns: (extracted_text, is_success, message)
    """
    if not file_bytes:
        return "", False, "The uploaded file is empty."
    
    try:
        stream = io.BytesIO(file_bytes)
        reader = PdfReader(stream)
        
        if len(reader.pages) == 0:
            return "", False, "PDF contains no pages."
            
        full_text = []
        for idx, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                full_text.append(text)
                
        joined_text = "\n".join(full_text).strip()
        if not joined_text:
            return "", False, "No selectable text found. The document may be an image scan."
            
        return joined_text, True, f"Successfully extracted {len(joined_text.split())} words across {len(reader.pages)} page(s)."
        
    except Exception as e:
        return "", False, f"Failed to parse PDF document: {str(e)}"
