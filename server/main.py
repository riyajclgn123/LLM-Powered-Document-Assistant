from fastapi import FastAPI, UploadFile, File
import pdfplumber

app = FastAPI()

@app.get("/")
def home():
    return {"message": "LLM Document Assistant API is running"}

@app.post("/extract-text/")
async def extract_text(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDF files are supported"}
    
    contents = await file.read()

    with open("temp.pdf", "wb") as f:
        f.write(contents)

    with pdfplumber.open("temp.pdf") as pdf:
        full_text = "\n".join(
            page.extract_text() for page in pdf.pages if page.extract_text()
        )

    return {"extracted_text": full_text}
