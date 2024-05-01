import pytesseract
from PIL import Image
import cv2
import os
import io


# Path to the Tesseract executable (update this based on your installation)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def extract_text_from_image(image_path):
    try:
        with Image.open(image_path) as img:
            text = pytesseract.image_to_string(img, lang='vie')
            return text
    except Exception as e:
        print(f"Error: {e}")
        return None


def preprocessing_image(image_path):
    filename = "{}.png".format(os.getpid())

    image = cv2.imread(image_path)
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    img = cv2.threshold(
        img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    cv2.imwrite("tmp/" + filename, img)
    return "tmp/" + filename


def get_filenames_in_folder(folder_path):
    filenames = []
    for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, filename)):
            filenames.append(folder_path + "/" + filename)
    return filenames


def test():
    file = preprocessing_image("img/img.jpg")
    extracted_text = extract_text_from_image(file)
    print(extracted_text)


def main():
    filenames = get_filenames_in_folder("img")
    for filename in filenames:
        file = preprocessing_image(filename)
        extracted_text = extract_text_from_image(file)
        if extracted_text:
            fn, extension = os.path.splitext(os.path.basename(filename))

            with io.open("text/" + fn + ".txt", "w", encoding="utf-8") as f:
                f.write(extracted_text)
            print("Success: " + filename)
        else:
            print("Failed:  " + filename)


if __name__ == "__main__":
    main()
    # test()
