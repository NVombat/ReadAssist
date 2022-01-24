#Imports
from PIL import Image
import pytesseract
import re

def get_text(path : str):
    myvar = pytesseract.image_to_string(Image.open(path))
    para = list(filter(lambda x: x != "" and len(re.sub(r" ", "", x)) != 0, myvar.split("\n")))
    return para