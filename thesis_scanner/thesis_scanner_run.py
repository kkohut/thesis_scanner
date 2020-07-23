import os
import sys
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'thesis_scanner'))
import cv2
# import GUI
# import take_picture
import timestamp
import picture_quality_improve
import alignImage
import rotate_image_180
import text_analysis
import deadline_validity
import date_validity


def main():
    # GUI starten [Immer an]
    # GUI()

    # Bild aufnehmen
    # image = take_picture.process()
    # cv2.imwrite("thesis_scanner_run_savedImage", image)

    # Thesis Liste einlesen [abs_file_path = Pfad zur Thesis Liste]
    script_dir = os.path.dirname(__file__)
    rel_path = "../data/thesis_data.txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    thesis_data = text_analysis.read_thesis_data(abs_file_path)

    # Bildverbesserung
    # rel_path = "thesis.png"  # for use with GUI
    rel_path = "../data/Test_GruenwaldB.jpeg"
    # rel_path = "../data/testMitFolie08.jpg"
    # rel_path = "../data/testAufKopf02.jpg"
    abs_file_path = os.path.join(script_dir, rel_path)
    image = cv2.imread(abs_file_path)

    # Bild gerade ausrichten
    image, _, _ = alignImage.align_image(image)
    cv2.imwrite("thesis_scanner_run_alignedImage.jpg", image)

    # Bild verbessern
    image = picture_quality_improve.picture_quality_improve(image)
    cv2.imwrite("thesis_scanner_run_improvedImage.jpg", image)

    # Bild auf hochkante Ausrichtung prüfen
    image, extracted_text = rotate_image_180.rotate_input(image)
    cv2.imwrite("thesis_scanner_run_uprightImage.jpg", image)

    # Pytesseract
    print("___________________________________________________________________________________________________________")
    print("EINGELESENER TEXT:\n", extracted_text)

    # Text herausziehen
    critical_lines = text_analysis.filter_string(extracted_text)

    # Textanalyse
    print("___________________________________________________________________________________________________________")
    print("\nLISTE VOR DER ANALYSE:\n")
    text_analysis.print_all_theses(thesis_data)
    found_thesis = text_analysis.find_thesis(critical_lines, thesis_data)
    found_thesis.deadline = date_validity.get_date(extracted_text.splitlines(), found_thesis.title)

    # Timestamp speichern
    found_thesis.time_handed_in = timestamp.get_timestamp()
    print("___________________________________________________________________________________________________________")
    print("\nLISTE NACH DER ANALYSE:\n")
    text_analysis.print_all_theses(thesis_data)
    print("___________________________________________________________________________________________________________")
    print("\nERKANNTE ARBEIT:")
    text_analysis.print_thesis(found_thesis, thesis_data)

    # Deadline auslesen
    # deadline = deadline_validity.get_deadline(extracted_text)
    # print(deadline_validity.test_validity(timeStamp))
    return found_thesis.author.name, found_thesis.title


if __name__ == "__main__":
    main()
