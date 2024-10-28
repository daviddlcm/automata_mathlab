def extract_text_txt(file_path):
    with open(file_path, 'r') as file:
        text = file.read()

    words = text.split()


    return " ".join(words)
