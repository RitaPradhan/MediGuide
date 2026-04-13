import re
from openai import OpenAI
import os

client = OpenAI(api_key="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")
def predict_disease(symptoms):
    symptoms_lower = symptoms.lower()

    if re.search(r'fever|cough|headache', symptoms_lower):
        return 'Common Cold'
    elif re.search(r'chest pain|shortness of breath', symptoms_lower):
        return 'Heart Disease'
    elif re.search(r'nausea|vomiting|diarrhea', symptoms_lower):
        return 'Food Poisoning'
    
    return 'Unknown'


def ai_analysis(symptoms):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a medical assistant."},
                {"role": "user", "content": symptoms}
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        print("ERROR:", e)
        return str(e)