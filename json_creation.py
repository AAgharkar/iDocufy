import io

from google.cloud import vision
from google.cloud.vision import types

client = vision.ImageAnnotatorClient()

    # [START migration_text_detection]
with io.open('static/ADP Example 101817-1.jpg', 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

response = client.text_detection(image=image)
texts = response.text_annotations
print('Texts:')

for text in texts:
    print('\n"{}"'.format(text.description))

    vertices = (['({})'.format(vertex.x,vertex.y)
                for vertex in text.bounding_poly.vertices])
# print(vertices)
    print('bounds: {}'.format(','.join(vertices)))