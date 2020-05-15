import cv2
import pytesseract as tess

#image = cv2.imread(r"C:\Users\alexb\Documents\thesis-scanner\data\testOhneFolie08.jpg")



def getImageWithBoundingBoxes(image):
    """

    :param boxes: List with the following columns
    dict_keys(['level', 'page_num', 'block_num', 'par_num', 'line_num', 'word_num', 'left', 'top', 'width', 'height', 'conf', 'text'])
    :return:
    """
    textBoxes = tess.image_to_data(image, "deu")

    for x, b in enumerate(textBoxes.splitlines()):  # enumarate counts the lines

        if (x != 0):  # dont need the first line
            b = b.split()  # lines with words does have 12 columns, without words only 11
            if (len(b) == 12):
                print(b)
                x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                cv2.rectangle(image, (x - 3, y - 3), (w + x + 3, h + y + 3), (0, 127, 255), 3)
    return image


# getImageWithBoundingBoxes(image)
# cv2.namedWindow("Result", cv2.WINDOW_NORMAL)
# cv2.imshow("Result", image)
# cv2.waitKey()
