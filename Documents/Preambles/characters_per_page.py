import PyPDF2

def count_characters_in_pdf(file_path):
    # Open the PDF file
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        
        # Initialize character count
        char_count = 0
        
        # Iterate through each page and count characters
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text = page.extract_text()
            char_count += len(text)

        char_count = char_count / num_pages
        
        return char_count

# Path to your PDF file
pdf_file_path = '../Preambles/test.pdf'

# Count characters and print result
count = count_characters_in_pdf(pdf_file_path)
print(f"Total number of characters (including spaces): {count}")
