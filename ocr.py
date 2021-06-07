import pytesseract
pytesseract.pytesseract.tesseract_cmd = "tesseract/tesseract.exe"
import cv2
from PIL import Image
import numpy as np
class TextScanner():

    def __init__(self):
        pass

    def pre_process(self, image):
        self.grayscale = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        self.denoised = cv2.medianBlur(self.grayscale,1)
        self.thresholded = cv2.threshold(self.denoised, 0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        return self.thresholded

    def image_to_text(self, image):
        return pytesseract.image_to_string(image)


def test():
    test_img = np.array(Image.open("test.png"))
    scanner = TextScanner()
    processed = scanner.pre_process(test_img)
    cv2.imshow("image", processed)
    cv2.waitKey(0)
    print(scanner.image_to_text(scanner.thresholded))

if __name__ == '__main__':
    test()