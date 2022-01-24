# Imports
from pdf2image import convert_from_path
from .OCR import get_text

#Converts pdf to text
def get_pdf(path : str):
    #Stores all the pages of the pdf @500 pixel clarity
    pages =  convert_from_path(path, 500)

    for page in pages:
        filename = "page.jpg"
        page.save(filename, 'JPEG')
        text = get_text(filename)

    return text

if __name__ == '__main__':
    print(get_pdf("/home/nvombat/Desktop/ReadAssist/Resume.pdf"))