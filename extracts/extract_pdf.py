import PyPDF2

def extract_text_pdf(file_path):
    extract_text = []
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for no_page in reader.pages:
            extract_text.append(no_page.extract_text())
    text = " ".join(extract_text)
    
    text = text.replace('\n', ' ')  
    text = text.replace('\t', ' ')  
    text = ' '.join(text.split())   
    return text