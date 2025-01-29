from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import nltk
from fastapi.middleware.cors import CORSMiddleware

nltk.download("punkt")
nltk.download("punkt_tab")

def load_allowed_words(filename):
    allowed_words = set()
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            allowed_words.add(line.strip())
    return allowed_words

allowed_words = load_allowed_words('Words.txt')

def filter_message_nltk(message):
    tokens = nltk.word_tokenize(message)
    for token in tokens:
        if token not in allowed_words:
            return "لطفاً پیام را اصلاح کنید."
    
    return "پیام مجاز است."

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def get_form():
    return """
    <html>
        <head>
            <title>سیستم فیلتر پیام</title>
        </head>
        <body>
            <h1>سیستم فیلتر پیام</h1>
            <form action="/check" method="post">
                <label for="message">پیغام را وارد کنید</label><br>
                <textarea id="message" name="message" rows="4" cols="50"></textarea><br><br>
                <input type="submit" value="ارسال">
            </form>
        </body>
    </html>
    """

@app.post("/check")
async def check_message(message: str = Form(...)):
    result = filter_message_nltk(message.lower())
    return {"message": message, "allowed": result}
