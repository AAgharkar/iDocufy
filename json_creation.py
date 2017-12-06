import io

import flask
from flask import json
from google.cloud import vision
from google.cloud.vision import types

client = vision.ImageAnnotatorClient()

with io.open('static/ADP Example 101817-1.jpg', 'rb') as image_file:
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

    # print('bounds: {}'.format(','.join(vertices)))
#     response1={
#         "description":text.description,
#         "vertices":['x:{},y:{}'.format(vertex.x,vertex.y)
#                 for vertex in text.bounding_poly.vertices]
#     }
#     result.append(response1)
#
# with open('Image_Result.json','w') as f:
#     json.dump(result,f)
# with open('Image_Result.json','r') as f:
#     img=json.load(f)
#
# for items in img:
#     print(items['description'])
#     print(items['vertices'])
# print(img[2]['description'])


