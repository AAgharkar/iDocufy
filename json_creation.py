import io

import flask
from flask import json
from google.cloud import vision
import paystub_dn,Img_to_Text
from google.cloud.vision import types

client = vision.ImageAnnotatorClient()
image=paystub_dn.image_conversion_smooth(r"C:\Users\ankitaa\Desktop\Images\Valid Paystub\Paychex Template 2 - 102617pdf-1.jpg")
text=Img_to_Text.detect_document(image)
print(text)
with io.open(image, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

response = client.text_detection(image=image)
texts = response.text_annotations


result=[]
for text in texts[1:]:
    # print('\n"{}"'.format(text.description))

    vertices = ['X={},y={}'.format(vertex.x,vertex.y)
                for vertex in text.bounding_poly.vertices]

    data=({text.description:vertices})
    # print(data)



