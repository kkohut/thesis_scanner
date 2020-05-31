import cv2
import os
# import GUI
# import take_picture
# import timestamp
import picture_quality_improve
import alignImage
import Rotate_jpg_180
import text_analysis
import deadline_validity


def main():
    # GUI starten [Immer an]
    # GUI()

    # Bild aufnehmen
    # image = take_picture.process()
    # cv2.imwrite("thesis_scanner_run_savedImage", image)

    # Timestamp speichern
    # timeStamp = timestamp.get_timestamp()

    # Thesis Liste einlesen [abs_file_path = Pfad zur Thesis Liste]
    script_dir = os.path.dirname(__file__)
    rel_path = "../data/thesis_data.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    thesis_data = text_analysis.read_thesis_data(abs_file_path)

    # Bild Verbesserung
    # rel_path = "../data/testOhneFolie10.jpg"
    # rel_path = "../data/testMitFolie08.jpg"
    rel_path = "../data/testAufKopf02.jpg"
    abs_file_path = os.path.join(script_dir, rel_path)
    image = cv2.imread(abs_file_path)
    image = picture_quality_improve.picture_quality_improve(image)
    cv2.imwrite("thesis_scanner_run_improvedImage.jpg", image)

    # Bild gerade ausrichten
    image = alignImage.align_image(image)
    cv2.imwrite("thesis_scanner_run_alignedImage.jpg", image)

    # Bild auf hochkante Ausrichtung prüfen
    image, extracted_text = Rotate_jpg_180.rotate_input(image)
    cv2.imwrite("thesis_scanner_run_uprightImage.jpg", image)

    # Pytesseract
    #extracted_text = text_analysis.extract(image)
    print("___________________________________________________________________________________________________________")
    print("EINGELESENER TEXT:\n", extracted_text)

    # Text herausziehen
    essential_info = text_analysis.filter_string(extracted_text)

    # Textanalyse
    print("___________________________________________________________________________________________________________")
    print("\nLISTE VOR DER ANALYSE:\n")
    for thesis in thesis_data:
        text_analysis.print_thesis(thesis)
    found_thesis = text_analysis.find_thesis(essential_info, thesis_data)
    print("___________________________________________________________________________________________________________")
    print("\nLISTE NACH DER ANALYSE:\n")
    for thesis in thesis_data:
        text_analysis.print_thesis(thesis)

    print("___________________________________________________________________________________________________________")
    print("\nERKANNTE ARBEIT:")
    text_analysis.print_thesis(found_thesis)

    # Deadline auslesen
    # deadline = deadline_validity.get_deadline(extracted_text)
    # print(deadline_validity.test_validity(timeStamp))


if __name__ == "__main__":
    main()
