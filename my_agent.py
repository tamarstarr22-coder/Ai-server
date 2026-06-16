import os
# ייבוא הרכיבים הרלוונטיים מתוך הקובץ הנוכחי שלך date_tool.py
from date_tool import chat_with_tool, system

# רשימה גלובלית לשמירת ההיסטוריה, על מנת שהבוט יזכור את הקשר השיחה (למשל על איזו עיר מדובר)
messages_history = []

def run_weather_agent(user_input: str) -> str:
    """
    הפונקציה המרכזית שמקבלת את קלט המשתמש, מנהלת את ההיסטוריה ומפעילה את הסוכן.
    """
    global messages_history
    
    # אתחול הנחיית המערכת (System Prompt) בהודעה הראשונה של השיחה
    if not messages_history:
        messages_history.append({"role": "system", "content": system})
    
    # הוספת קלט המשתמש הנוכחי להיסטוריית השיחה
    messages_history.append({"role": "user", "content": user_input})
    
    try:
        # הפעלת הסוכן וקבלת אובייקט ה-JsonReAct המפורסר
        parsed_response = chat_with_tool(messages_history)
        
        # טיפול במקרה של זיהוי נושא מחוץ לתחום (Off-topic) 
        if parsed_response.Is_Off_Topic:
            return parsed_response.Output
        
        # הדפסת ה"מחשבות" של המודל לקונסול (עוזר מאוד להראות למורה שהמודל מבצע ReAct)
        if parsed_response.Thought:
            print(f"\n[AI Thought Process: {parsed_response.Thought}]")
            
        # הדפסת מערך פריטי הלבוש שחולץ בצורה מובנית
        if parsed_response.Clothing_Suggestions:
            print(f"[Wardrobe System Extracted: {', '.join(parsed_response.Clothing_Suggestions)}]")

        # שמירת התשובה הסופית של ה-AI בהיסטוריית ההודעות לטובת המשך השיחה
        messages_history.append({"role": "assistant", "content": parsed_response.Output})
        
        # החזרת הטקסט הידידותי למשתמש
        return parsed_response.Output

    except Exception as e:
        return f"שגיאה בעיבוד הנתונים: {str(e)}"