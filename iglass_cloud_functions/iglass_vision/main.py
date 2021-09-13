import base64

from google.cloud import vision
from google.cloud.vision_v1 import types

client = vision.ImageAnnotatorClient()

def vision_entry(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    request_json = request.get_json()
    vision_type = request_json["type"]
    image_b64 = request_json["image_b64"]

    if vision_type == "OCR":
        text_response = recognize_document(image_b64)
        return {"response": text_response}
    elif vision_type == "objection-recognition":
        recognition_response = recognize_labels(image_b64)
        return {"response": recognition_response}
    else:
        return {"response": "Try again"}


def recognize_text(image_b64):
    """
    recognizes text from images that might be contained in street signs, sign boards, items and etc.
    it returns the extracted text from the image which goes through a preprocessor to clean the extracted text

    :param image_path: file path to image to detect text and return the extracted text
    :type image_path: str
    :return: extracted_text
    :rtype: str
    """
    try:
        # decode image from bytes format
        image_content = base64.b64decode(image_b64)

        # Client image to execute Google Cloud Vision API tasks over
        image = types.Image(content=image_content)

        # response to an image annotation 'text detection' request (similar structure to a json file format)
        response = client.text_detection(image=image)
        text_annotations = response.text_annotations

        # full recognized text from the image
        extracted_text = text_annotations[0].description

        if response.error.message:
            raise Exception(response.error.message)

        return extracted_text
    except:
        raise Exception

def recognize_document(image_b64):
    """
    optimized to recognize text from document images and also handwritten images. It returns an extracted text
    which goes through a preprocessor to clean the extracted text

    :param image_path: path to the document image to detect text and return the extracted text
    :type image_path: str
    :return: extracted_text
    :rtype: str
    """

    try:
        # decode image from bytes format
        image_content = base64.b64decode(image_b64)

        # Client image to execute Google Cloud Vision API tasks over
        image = types.Image(content=image_content)

        # response to an image annotation 'document detection' request (similar structure to a json file format)
        response = client.document_text_detection(image=image)
        text_annotations = response.text_annotations

        if response.error.message:
            raise Exception('Error occured '.format(response.error.message))

        # full recognized text from the image
        extracted_text = text_annotations[0].description

        return extracted_text

    except:
        raise Exception
def recognize_labels(image_b64):
    """
    this module detects and extracts information about entities which are present in an image. It returns a
    list of descriptive information in an image

    :param image_path: path to the image to detect and extract labels
    :type image_path: str
    :return: extracted_label: labels extracted from the image
    :rtype: str
    """

    try:
        # decode image from bytes format
        image_content = base64.b64decode(image_b64)

        # Client image to execute Google Cloud Vision API tasks over
        image = types.Image(content=image_content)

        # response to an image annotation 'label detection' request (similar structure to a json file format)
        response = client.label_detection(image=image)
        label_annotations = response.label_annotations

        if response.error.message:
            raise Exception('Error occured '.format(response.error.message))

        response_score = {}  # a dictation with the label as key and accuracy score as value
        for label in label_annotations:
            response_score[label.description] = label.score
        detected_labels = ", ".join(response_score.keys())

        return detected_labels

    except:
        raise Exception
