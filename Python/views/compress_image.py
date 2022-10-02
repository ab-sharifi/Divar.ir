"""
This script using pillow library for compress images size 
for loading better in web 
"""

from PIL import Image

def compress_image(imgOBJ):
    img = Image.open(imgOBJ)
    height,width = img.size
    img = img.resize((height,width), Image.ANTIALIAS)
    return img