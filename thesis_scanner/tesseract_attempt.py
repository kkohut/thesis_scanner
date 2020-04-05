try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

print(pytesseract.get_tesseract_version())
print(pytesseract.image_to_string(image = Image.open("/home/vintuh/MEGA/Studium/Module/SS20/Programmierprojekt/Material/Testdateien/vorlage_word_thesis-0.jpeg"), lang = "deu"))