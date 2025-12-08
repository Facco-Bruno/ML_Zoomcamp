import json
import numpy as np
from io import BytesIO
from urllib import request
from PIL import Image
import onnxruntime as ort


MODEL_PATH = "hair_classifier_empty.onnx"


def download_image(url):
    with request.urlopen(url) as resp:
        buffer = resp.read()
    stream = BytesIO(buffer)
    img = Image.open(stream)
    return img


def prepare_image(img, target_size):
    if img.mode != "RGB":
        img = img.convert("RGB")
    img = img.resize(target_size, Image.NEAREST)
    return img


def preprocess_image(img):
    # Ajuste target_size conforme o modelo (mesmo que Q2)
    target_size = (128, 128)  # EXEMPLO! Troque pelos valores certos.

    img = prepare_image(img, target_size)

    x = np.array(img).astype("float32")

    # === ESCOLHA: use o MESMO pré-processamento do homework 8 ===
    # Exemplo 1: escalar para [0, 1] e normalizar com mean/std:
    x /= 255.0
    mean = np.array([0.485, 0.456, 0.406], dtype="float32")
    std  = np.array([0.229, 0.224, 0.225], dtype="float32")
    x = (x - mean) / std

    # Se você usou outra fórmula (ex: x/127.5 - 1), troque o bloco acima.

    # HWC -> CHW -> batch
    x = np.transpose(x, (2, 0, 1))
    x = np.expand_dims(x, axis=0)
    return x


# Criar sessão global para reaproveitar entre chamadas
session = ort.InferenceSession(MODEL_PATH, providers=["CPUExecutionProvider"])
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name


def predict(url: str) -> float:
    img = download_image(url)
    x = preprocess_image(img)
    y_pred = session.run([output_name], {input_name: x})[0]
    return float(y_pred[0])


def lambda_handler(event, context):
    """
    Espera um JSON assim:
    {
        "url": "https://....jpeg"
    }
    """
    url = event["url"]
    score = predict(url)
    return {
        "statusCode": 200,
        "body": json.dumps({"score": score})
    }
