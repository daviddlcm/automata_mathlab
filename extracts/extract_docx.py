import docx
def extract_text_docx(file_path):
    document = docx.Document(file_path)
    pages_text = []
    for p in document.paragraphs:
        text = p.text.strip()
        if text: 
            pages_text.append(text)
    return " ".join(pages_text)