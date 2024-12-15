from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from transformers import pipeline

# Load the fine-tuned model and tokenizer
model_path = "./distilbert_finetuned"  # Path to the folder containing model files
distilbert_pipeline = pipeline("text-classification", model=model_path, tokenizer=model_path)

# Initialize FastAPI app
app = FastAPI()

# Mount static files (e.g., CSS, JS, index.html)
app.mount("/static", StaticFiles(directory="."), name="static")

# Define the input schema
class InputText(BaseModel):
    text: str

@app.post("/predict/")
async def predict(input: InputText):
    # Use the pipeline to predict
    predictions = distilbert_pipeline(input.text)
    label = predictions[0]["label"]  # Directly use the raw label (LABEL_0 or LABEL_1)
    confidence = predictions[0]["score"]

    # Ensure confidence is formatted correctly
    confidence_percentage = round(confidence * 100, 2)

    return {
        "text": input.text,
        "prediction": label,  # Return the raw label (LABEL_0 or LABEL_1)
        "confidence": f"{confidence_percentage}%"
    }



# Serve the index.html
@app.get("/", response_class=HTMLResponse)
async def serve_index():
    with open("index.html") as f:
        return HTMLResponse(content=f.read())


from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8090"],  # Update with the frontend's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
