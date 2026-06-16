import os
import json
import requests
from openai import OpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# טעינת משתני סביבה מהקובץ .env
load_dotenv()

# א. הגדרת מבנה הפלט המובנה (Structured Outputs) בהתאם לדרישות המטלה [cite: 9]
class JsonReAct(BaseModel):
    Thought: str = Field(description="The bot's internal explanation of why it chooses to perform an action or what its clothing considerations are")
    Action: str = Field(description="'get_weather_data' if the weather tool needs to be run, or 'Final Answer' if there is a ready answer")
    Is_Off_Topic: bool = Field(description="Boolean variable - True if the user asked a question not related to weather or clothing")
    Clothing_Suggestions: list[str] = Field(description="A detailed list of recommended clothing items e.g.: ['raincoat', 'umbrella', 'boots']")
    Output: str = Field(description="The final, polite, genuine, and friendly answer you will present to the user")

# ב. פונקציה מותאמת אישית (Custom Tool) לשליפת מזג אוויר חי בזמן אמת [cite: 10]
def get_weather_data(city: str) -> str:
    """
    פונקציה המבצעת קריאה ל-API חיצוני ומחזירה את נתוני מזג האוויר הנוכחיים עבור עיר מסוימת.
    """
    # שליפת המפתח מקובץ ה-.env (מתאים לשם WEATHER_API שמופיע אצלך בקובץ)
    api_key = os.getenv("WEATHER_API") 
    if not api_key:
        return "שגיאה: מפתח ה-API של מזג האוויר (WEATHER_API) אינו מוגדר כראוי בקובץ .env"
    
    # כתובת הבסיס של ה-API (ללא שרשור ידני של משתנים)
    url = "http://api.openweathermap.org/data/2.5/weather"
    
    # העברת הפרמטרים בצורה בטוחה דרך מילון params.
    # מנגנון זה מבצע קידוד (URL Encoding) אוטומטי לרווחים ואותיות בעברית!
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
        "lang": "he"
    }
    
    try:
        # ביצוע קריאת ה-GET עם הפרמטרים המקודדים
        response = requests.get(url, params=params, timeout=5)
        
        # --- בלוק דיאגנוסטיקה (DEBUG) למפתח ---
        # שורות אלו ידפיסו לך בתוך הטרמינל בדיוק מה השרת עונה, מבלי שהמשתמש בצ'אט יראה זאת.
        print(f"\n--- [DEBUG WEATHER API] ---")
        print(f"City requested by model: '{city}'")
        print(f"Response Status Code: {response.status_code}")
        if response.status_code != 200:
            print(f"Response Error Message from server: {response.text}")
        print(f"---------------------------\n")
        # --------------------------------------
        
        # אם התגובה תקינה (קוד 200)
        if response.status_code == 200:
            data = response.json()
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            humidity = data["main"]["humidity"]
            return f"ב{city} כעת {temp} מעלות, {description} עם {humidity}% לחות."
            
        # אם חזר קוד שגיאה (כמו 401 או 404), נחזיר פירוט למודל כדי שיבין את מהות התקלה
        return f"לא הצלחתי למצוא נתוני מזג אוויר עבור המיקום: {city}. קוד שגיאה מהשרת: {response.status_code}."
        
    except Exception as e:
        return f"שגיאה בתקשורת מול שרת מזג האוויר: {str(e)}"
# אתחול הלקוח של OpenAI (עושה שימוש אוטומטי ב-OPENAI_API_KEY מתוך ה-.env) 
client = OpenAI()

# ג. הגדרת כלי ה-Function Calling עבור המודל
tools = [
 {
    "type": "function",
    "function": {
        "name": "get_weather_data",
        "description": "Retrieves the latest real-time weather data for a given city or location",
        "strict": True, 
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The name of the city or location the user specified (e.g. Jerusalem, Tel Aviv)"
                }
            },
            "additionalProperties": False,
            "required": ["city"] 
        }
    }
}
]

# ד. הנחיית המערכת (System Prompt) - הגדרת גבולות הגזרה וחסימת נושאים (Off-topic prevention) [cite: 5, 14, 22]
system = """
You are a smart and professional wardrobe and weather assistant in the SmartWear AI app. [cite: 4]
Your sole role is to recommend to users what to wear or how to organize themselves depending on the weather outside. [cite: 4, 13]
If you need to know the weather to answer, set Action='get_weather_data'.
If you have all the information, set Action='Final Answer' and write your answer in Output.

Hard mandatory requirement of the system (Off-topic prevention)[cite: 5, 14, 22]:
You should make sure you only answer questions related to weather, clothing, footwear, or recommendations for appropriate outdoor activities (such as going to the beach or hiking). [cite: 5, 13]
If the user asks about any other topic (for example: recipes, history, help writing code, or politics) - [cite: 21]
You should set the Is_Off_Topic field to True, set Action='Final Answer', and in the Output field politely decline 
and state that you are not authorized to answer topics outside the scope of the application. [cite: 5]
"""

# ה. פונקציית הרצה רקורסיבית מול OpenAI התומכת בהפעלת הכלים ובפלט המובנה
def chat_with_tool(messages_history):
    response = client.chat.completions.parse(
        model="gpt-4.1-mini",
        messages=messages_history,
        tools=tools,
        response_format=JsonReAct # אכיפת מבנה הפלט המובנה שהגדרנו [cite: 9]
    )
    
    assistant_message = response.choices[0].message
    stepObj = assistant_message.parsed

    # בדיקה האם המודל החליט שהוא צריך להפעיל כלי (Function Calling)
    if assistant_message.tool_calls:
        messages_history.append(assistant_message)
        
        for tool_call in assistant_message.tool_calls:
            function_name = tool_call.function.name
            function_to_call = globals().get(function_name)
            function_args = json.loads(tool_call.function.arguments)
            
            # הפעלת פונקציית מזג האוויר וקבלת התוצאה מהרשת
            result = function_to_call(**function_args)
            
            # הזנת תוצאת הכלי בחזרה להיסטוריית ההודעות של המודל
            messages_history.append({
                "tool_call_id": tool_call.id, 
                "role": "tool",
                "name": function_name,
                "content": result
            })
            
        # קריאה חוזרת (רקורסיבית) למודל כדי שיעבד את נתוני מזג האוויר שקיבל וינסח תשובה
        return chat_with_tool(messages_history)
        
    return stepObj