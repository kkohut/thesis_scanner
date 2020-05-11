import cv2
import pytesseract as tess

img = cv2.imread(r"C:\Users\alexb\Documents\thesis-scanner\data\testOhneFolie08.jpg")
hImg, wImg, _ = img.shape  # returns rows, columns and channels(colour)
textBoxes = tess.image_to_data(img, "deu")


def getImageWithBoundingBoxes(boxes):
    """

    :param boxes: List with the following columns
    dict_keys(['level', 'page_num', 'block_num', 'par_num', 'line_num', 'word_num', 'left', 'top', 'width', 'height', 'conf', 'text'])
    :return:
    """

    for x, b in enumerate(textBoxes.splitlines()):  # enumarate counts the lines

        if (x != 0):  # dont need the first line
            b = b.split()  # lines with words does have 12 columns, without words only 11
            if (len(b) == 12):
                print(b)
                x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                cv2.rectangle(img, (x - 3, y - 3), (w + x + 3, h + y + 3), (0, 127, 255), 3)


getImageWithBoundingBoxes(textBoxes)

cv2.namedWindow("Result", cv2.WINDOW_NORMAL)
cv2.imshow("Result", img)
cv2.waitKey()
