#Import pytesseract libraries and regex
import pytesseract
from PIL import Image
import re

def get_text(path : str):
    #Convert image to string
    #print("printing path", path)
    myvar = pytesseract.image_to_string(Image.open(path))
    #Convert text into paragraphs
    para = list(filter(lambda x: x != "" and len(re.sub(r" ", "", x)) != 0, myvar.split("\n")))
    #Return list of paragraphs
    return para