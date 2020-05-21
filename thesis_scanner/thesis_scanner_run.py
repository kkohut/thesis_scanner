import cv2
import os
#import GUI     # erstmal ohne GUI zum Laufen bringen
import take_picture
import timestamp
import picture_quality_improve
import alignImage
import Rotate_jpg_180
import text_analysis
import deadline_validity

# while(true) ergänzen
def main():
    # GUI starten [Immer an]
    #GUI()


    # Bild aufnehmen
    #image = take_picture.process()     # erstmal ohne Foto zum Laufen bringen
    #cv2.imwrite("thesis_scanner_run_savedImage", image)


    # Timestamp speichern   # erstmal ohne TimeStamp zum Laufen bringen
    #timeStamp = timestamp.get_timestamp()


    # Thesis Liste einlesen [abs_file_path = Pfad zur Thesis Liste]
    script_dir = os.path.dirname(__file__)
    rel_path = "../data/thesis_data.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    thesis_data = text_analysis.read_thesis_data(abs_file_path)


    # Bild Verbesserung
    image = picture_quality_improve.__()
    cv2.imwrite("thesis_scanner_run_improvedImage", image)


    # Bild gerade ausrichten
    image = alignImage.align_image(image)
    cv2.imwrite("thesis_scanner_run_alignedImage", image)


    # Bild auf hochkante Ausrichtung prüfen
    image = Rotate_jpg_180.rotate_input(image)
    cv2.imwrite("thesis_scanner_run_uprightImage", uprightImage)


    # Pytesseract
    extractedText = text_analysis.extract(cv2.imread("path to saved picture"))


    # Text herausziehen
    essentialInfo = text_analysis.filter_string(extractedText)


    # Textanalyse [Thesis Class = .author und .title] [Liste = thesis_data]
    foundThesis = text_analysis.find_thesis(essentialInfo, thesisData)


    # Deadline auslesen
    deadline = deadline_validity.get_deadline(extractedText)
    print(deadline_validity.test_validity(timeStamp))


if __name__ == "__main__":
    main()