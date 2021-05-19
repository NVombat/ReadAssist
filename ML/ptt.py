# Import libraries 
from PIL import Image 
import pytesseract 
import sys 
from pdf2image import convert_from_path 

#Import function that converts images to text from OCR.py (. symbolyses the same directory)
from .OCR import get_text
import re
import os 
  
#Converts pdf to text
def get_pdf(path : str):
    #Stores all the pages of the pdf @500 pixel clarity
    pages =  convert_from_path(path, 500)
    #For each page
    for page in pages:
        #Create a jpeg file (Which gets overwritten for every page)
        filename = "page.jpg"
        #Save the image
        page.save(filename, 'JPEG')
        #convert image to text and return that text
        text = get_text(filename)
    return text
if __name__ == '__main__':
    #Print the text when pdf path is passed to function
    print(get_pdf("/home/nvombat/Desktop/ReadAssist/Resume.pdf"))