import io
import os
import cv2
import numpy as np
from shapely.geometry import Polygon
import cv2

def detect_handwritten_ocr(path):
    """Detects handwritten characters in a local image.

    Args:
    path: The path to the local file.
    """
    
    img = cv2.imread(path)
    height, width, channels = img.shape

    from google.cloud import vision_v1p3beta1 as vision
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    
    image = vision.Image(content=content)
    
    # Language hint codes for handwritten OCR:
    # en-t-i0-handwrit, mul-Latn-t-i0-handwrit
    # Note: Use only one language hint code per request for handwritten OCR.
    image_context = vision.ImageContext(
        language_hints=['en-t-i0-handwrit'])

    response = client.document_text_detection(image=image, image_context=image_context)

    return response

def display_detected_handwritten(path, response, filename):
    img = cv2.imread(path)
    height, width, channels = img.shape

    result = []
    for index, text in enumerate(response.text_annotations):
        if(index == 0):
            result.append({
                'text': text.description,
                'text_point': 'full text'
            })
            continue
        x = []
        y = []
        for coords in text.bounding_poly.vertices:
            x.append(coords.x)
            y.append(coords.y)
        poly_points = np.array([[x[0], y[0]], [x[1], y[1]], [x[2], y[2]], [x[3], y[3]]], np.int32)
        poly_points = poly_points.reshape((-1, 1, 2))

        # set random color
        color = (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))
        thickness = 2
        text = text.description            
        text_point = (x[3]+1, y[3]+20)
        img = cv2.polylines(img, [poly_points], True, color, thickness)
        img = cv2.putText(img, text, text_point , cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color)
        
        poly_points = [[x[0], y[0]], [x[1], y[1]], [x[2], y[2]], [x[3], y[3]]]

        result.append({
            'text': text,
            'poly_points': poly_points,
            'text_point': text_point,
            'color': color
        })
    cv2.imwrite('./output/' + filename, img)
    # cv2.imshow('img', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return result
            
            
            