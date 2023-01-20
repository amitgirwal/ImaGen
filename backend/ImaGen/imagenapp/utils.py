import cv2


def compressImage(image, action):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    print("Not Filter......")
    if action == 'NO_FILTER':
        filtered = image
    return filtered

def get_filtered_image(image, action):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    filtered = None

    # if action == 'PNG':
    #     filtered = image
    #     cv2.imwrite(filename, img)
    #     return filtered
    if action == 'NO_FILTER':
        filtered = image
    elif action == 'COLORIZED':
        filtered = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    elif action == 'GRAYSCALE':
        filtered = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif action == 'BLURRED':
        width, height = img.shape[:2]
        if width > 500:
            k = (50, 50)
        elif width > 200 and width <=500:
            k = (25,25)
        else:
            k = (10,10)
        blur = cv2.blur(img, k)
        filtered = cv2.cvtColor(blur, cv2.COLOR_BGR2RGB)
    elif action == 'BINARY':
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, filtered = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    elif action == 'INVERT':
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, img = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
        filtered = cv2.bitwise_not(img)
    return filtered


from PIL import Image
import os

def convert_to_webp(filename, path="images/"):
    extension = filename.split('.')[-1]
    fname = filename.split('.')[0]
    img = Image.open(path + filename)

    if extension == "png":
        img.save((path+fname+".webp"), "webp", lossless=True)
    elif extension == "jpg" or extension == "jpeg":
        img.save((path+fname+".webp"), "webp", quality=85)

def convert_all(path="images/"):
    for root, dirs, files in os.walk(path):
        for imagefile in files:
            if imagefile.endswith(".png") or imagefile.endswith(".jpg") or imagefile.endswith(".jpeg"):
                convert_to_webp(imagefile, os.path.join(root, ""))

 