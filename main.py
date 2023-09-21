from dotenv import load_dotenv
from datetime import datetime
import os
import requests

load_dotenv()
APP_ID = os.environ.get("NUTRITIONIX_APPLICATION_ID")
APP_KEY = os.environ.get("NUTRITIONIX_APPLICATION_KEY")
SHEETY_AUTH_TOKEN = os.environ.get("SHEETY_AUTH_TOKEN")
SHEETY_END_POINT = os.environ.get("SHEETY_END_POINT")
END_POINT = " https://trackapi.nutritionix.com/v2/natural/exercise"
headers = {
    "x-app-id": APP_ID,
    "x-app-key": APP_KEY,
    "x-remote-user-id": "0",
}

is_on = True
while is_on:
    user_input = input("Tell us what exercise you have done today(Type 'exit' to exit): ")
    if user_input == 'exit':
        is_on = False
    elif user_input:
        nutriment_parameters = {
            "query": user_input,
            "gender": "female",
            "weight_kg": 72.5,
            "height_cm": 167.64,
            "age": 30
        }
        response = requests.post(url=END_POINT, json=nutriment_parameters, headers=headers)
        user_data_response = response.json()['exercises'][0]
        exercise = user_data_response['name'].capitalize()
        duration = user_data_response['duration_min']
        calories_consumed = user_data_response['nf_calories']
        today = datetime.now()
        date = [today.strftime("%d/%m/%Y"), today.strftime("%H:%M:%S")]
        body = {
            "workout": {
                "date": date[0],
                "time": date[1],
                "exercise": exercise,
                "duration": duration,
                "calories": calories_consumed,
            }
        }
        response = requests.post(url=SHEETY_END_POINT, json=body, headers={"Authorization": SHEETY_AUTH_TOKEN})
        print(response.text)
    print(SHEETY_AUTH_TOKEN)
