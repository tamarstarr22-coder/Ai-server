from openai import OpenAI
import datetime

def get_current_date():
    return datetime.date.today().strftime("%y-%m-%d")


tools = [
{
    "type": "function",
    "function": {
        "name": "get_current_date",
        "description": "Returns the current date in YY-MM-DD format",
        "strict": True, # הפעלת מצב Strict
        "parameters": {
            "type": "object",
            "properties": {}, # גם כשריק, חייב להיות אובייקט
            "additionalProperties": False, # חובה במצב Strict
            "required": [] # חובה במצב Strict (רשימה ריקה אם אין פרמטרים)
        }
    }
}
]


client = OpenAI()

def start_chat():
    #system_prompt="You are a very nervous, impatient agent. You answer each question in a maximum of two sentences. Don't show any empathy. Make sure the user is not satisfied with your answer.:Use harsh words.For example:Make me coffeeMake it yourself, you lazy person."
    #history=[{"role": "system", "content": system_prompt}]
    history=[]
    while(True):
        user_input = input("User: ")
        if(user_input=="."):
            break

        history.append({"role": "user", "content": user_input})

        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",  
                messages=history
            )
            ai_message = response.choices[0].message.content
            print(f"AI: {ai_message}")
            history.append({"role": "assistant", "content": ai_message})
        except Exception as e:
            print(f"ERROR: {e}")
             
start_chat()

