# ייבוא פונקציית ההרצה מתוך קובץ הסוכן שלך (my_agent.py)
from server.my_agent import run_weather_agent

def start_chat():
    print("==================================================")
    print("   Welcome to SmartWear AI - Wardrobe Assistant!   ")
    print("   (Type '.' and press Enter to exit)             ")
    print("==================================================")
    
    while True:
        try:
            # קליטת הודעה מהמשתמש
            user_input = input("\nUser: ")
            
            # בדיקת יציאה רגילה ומתוכננת מהתוכנית באמצעות הקשת נקודה
            if user_input.strip() == ".":
                print("Thank you for using SmartWear AI! Goodbye.")
                break
            
            # התעלמות מהודעות ריקות (אם המשתמש רק לחץ Enter בטעות)
            if not user_input.strip():
                continue
                
            print("AI is thinking...")
            
            # הפעלת הסוכן החכם המעובד שלנו מתוך my_agent.py
            response = run_weather_agent(user_input)
            
            # הצגת התשובה הסופית והידידותית למשתמש
            print(f"\nAI: {response}")
                
        except KeyboardInterrupt:
            # תפיסה מתוחכמת של עצירה ידנית מהמקלדת (כמו Ctrl+C)
            # במקום להציג שגיאה אדומה ומלחיצה, נפרד מהמשתמש בנימוס ונצא מהלולאה
            print("\n\n[System Info] Program interrupted by user. Thank you for using SmartWear AI! Goodbye.")
            break
            
        except Exception as e:
            # תפיסת שאר השגיאות הכלליות ומניעת קריסה (כמו בעיות רשת, שגיאות API וכו')
            print(f"\nERROR: An unexpected error occurred: {e}")

if __name__ == "__main__":
    start_chat()