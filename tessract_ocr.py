import re
# import commands
import subprocess

def get_number_plate_data(imagepath):
	command = 'tesseract ' + imagepath + ' stdout --tessdata-dir C:/Program Files/Tesseract-OCR/tessdata --psm 7'
	tesseractResult = subprocess.run(command.split(' '), stdout=subprocess.PIPE).stdout.decode('utf-8')
	print(tesseractResult)

if __name__ == '__main__':
	get_number_plate_data(r"Upload_Image/ct_dl_example_091117.jpg")
