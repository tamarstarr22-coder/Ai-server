from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# 1. יצירת מופע האפליקציה (זהו ה-'app' ש-uvicorn מחפש!)
app = FastAPI()

# 2. הגדרת CORS - מאפשר ל-React (שמריץ את עצמו בדרך כלל על פורט 5173 או 3000) לגשת לשרת הפייתון
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # במוד פיתוח מאפשרים לכל המקורות להתחבר
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# הגדרת מבנה הנתונים שהשרת מצפה לקבל מה-React
class MessageRequest(BaseModel):
    message: str

# 3. נקודת קצה לבדיקה שהשרת עובד
@app.get("/")
def read_root():
    return {"status": "success", "message": "Backend server is running smoothly!"}

# 4. נקודת קצה לקבלת הודעות מהצ'אט של ה-React
@app.post("/api/chat")
def chat_endpoint(request: MessageRequest):
    user_text = request.message
    
    # כאן בהמשך נחבר את הלוגיקה מתוך chat.py כדי להחזיר תשובה מה-AI
    # כרגע נחזיר תשובת דמה (Mock) כדי לוודא שהחיבור עובד
    ai_response = f"קיבלתי את ההודעה שלך: '{user_text}'. השרת מחובר בהצלחה!"
    
    return {"response": ai_response}