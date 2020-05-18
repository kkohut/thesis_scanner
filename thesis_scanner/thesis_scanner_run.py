import cv2
import GUI
import take_picture
import timestamp
import picture_quality_improve
import alignImage
import Rotate_jpg_180.py
import text_extraction
import text_analysis
import deadline_validity


# while(true) ergänzen
def main():
    # GUI starten [Immer an]
    GUI()


    # Bild aufnehmen
    image = take_picture.process()
    cv2.imwrite("thesis_scanner_run_savedImage", image)


    # Timestamp speichern
    timeStamp = timestamp.get_timestamp()


    # Thesis Liste einlesen [abs_file_path = Pfad zur Thesis Liste]
    thesisData = text_analysis.read_thesis_data(absFilePath)


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
    extractedText = text_extraction.extract(cv2.imread("path to saved picture"))


    # Text herausziehen
    essentialInfo = text_analysis.filter_string(extractedText[0])


    # Textanalyse [Thesis Class = .author und .title] [Liste = thesis_data]
    foundThesis = text_analysis.find_thesis(essentialInfo, thesisData)


    # Deadline auslesen
    deadline = deadline_validity.get_deadline(extractedText)
    print(deadline_validity.test_validity(timeStamp))


if __name__ == "__main__":
    main()