import os
import sys

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'thesis_scanner'))
import cv2
import timestamp
import picture_quality_improve
import alignImage
import rotate_image_180
import text_analysis
import date_validity
import logging

logging.basicConfig(filename="../data/logs/scan_results.log", level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s: %(message)s",
                    datefmt="%d/%m/%Y %H:%M:%S")

# Thesis Liste einlesen [abs_file_path = Pfad zur Thesis Liste]
script_dir = os.path.dirname(__file__)
rel_path = "../data/thesis_data.txt"
abs_file_path = os.path.join(script_dir, rel_path)
thesis_data = text_analysis.read_thesis_data(abs_file_path)


def main():
    # Bild einlesen
    rel_path = "thesis.png"
    abs_file_path = os.path.join(script_dir, rel_path)
    image = cv2.imread(abs_file_path)

    # Bild gerade ausrichten
    image, _, _ = alignImage.align_image(image)

    # Bild verbessern
    image = picture_quality_improve.picture_quality_improve(image)

    # Bild auf hochkante Ausrichtung prüfen
    image, extracted_text = rotate_image_180.rotate_input(image)

    # Demo: Liste auf Konsole ausgeben
    print("___________________________________________________________________________________________________________")
    print("EINGELESENER TEXT:\n", extracted_text)

    # Text herausziehen
    critical_lines = text_analysis.filter_string(extracted_text)

    # Textanalyse
    print("___________________________________________________________________________________________________________")
    print("\nLISTE VOR DER ANALYSE:\n")
    text_analysis.print_all_theses(thesis_data)
    found_thesis = text_analysis.find_thesis(critical_lines, thesis_data)
    try:
        found_thesis.deadline = date_validity.get_date(extracted_text.splitlines(), found_thesis.title)
    except RuntimeError:
        logging.warning("Date could not be found")

    # Timestamp speichern
    found_thesis.time_handed_in = timestamp.get_timestamp()
    print("___________________________________________________________________________________________________________")
    print("\nLISTE NACH DER ANALYSE:\n")
    text_analysis.print_all_theses(thesis_data)
    print("___________________________________________________________________________________________________________")
    print("\nERKANNTE ARBEIT:")
    text_analysis.print_thesis(found_thesis, thesis_data)

    return found_thesis.author.name, found_thesis.title


if __name__ == "__main__":
    main()
