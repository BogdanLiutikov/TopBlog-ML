from PIL import Image
from fastapi import FastAPI, UploadFile
from ml import model_predict

app = FastAPI()


@app.post('/predict/')
def predict(image: UploadFile, platform: str):
    image = Image.open(image.file)
    return model_predict(image, platform)
