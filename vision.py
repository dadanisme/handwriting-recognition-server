from setup import *


path = './input/handwritten.jpeg'
response = detect_handwritten_ocr(path)
# print(response)
display_detected_handwritten(path, response, 'handwritten.jpeg')