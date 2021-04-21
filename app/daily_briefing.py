# app/daily_briefing.py

import os
from dotenv import load_dotenv
from datetime import date

from app import APP_ENV
from app.weather_service import get_hourly_forecasts, set_geography
from app.email_service import send_email

load_dotenv()

USER_NAME = os.getenv("USER_NAME", default="Player 1")


if __name__ == "__main__":

    print(f"RUNNING THE DAILY BRIEFING APP IN {APP_ENV.upper()} MODE...")

    # CAPTURE INPUTS

    user_country, user_zip, unit = set_geography()
    print("COUNTRY:", user_country)
    print("ZIP CODE:", user_zip)
    print("UNIT:", unit)

    # FETCH DATA

    result = get_hourly_forecasts(country_code=user_country, zip_code=user_zip, unit=unit)
    if not result:
        print("INVALID GEOGRAPHY. PLEASE CHECK YOUR INPUTS AND TRY AGAIN!")
        exit()

    # DISPLAY OUTPUTS

    todays_date = date.today().strftime('%A, %B %d, %Y')
    html = "<html>"
    html += f"<h3>Good Morning, {USER_NAME}!</h3>"
    html += "<h4>Today's Date</h4>"
    html += f"<p>{todays_date}</p>"
    html += f'<h2>Weather Forecast for {result["city_name"]}</h2>'
    html+= f'<p>Zip Code: {user_zip}</p>'
    html+= '<table style="width:100%">'
    html+= '<tr style="border-bottom:1px solid #ddd">'
    html+= '<th style="text-align:center">Time</th>'
    html+= '<th style="text-align:center">Temprature</th>'
    html+= '<th style="text-align:center">Conditions</th>'
    html+= '<th style="text-align:center">Icon</th>'
    html+= '</tr>'
    for forecast in result["hourly_forecasts"]:
        html+= '<tr style="border-bottom:1px solid #ddd">'
        html+= f'<td style="text-align:center">{ forecast["timestamp"] }</td>'
        html+= f'<td style="text-align:center">{ forecast["temp"] }</td>'
        html+= f'<td style="text-align:center">{ forecast["conditions"].upper() }</td>'
        html+= f'<td style="text-align:center"><img src="{ forecast["image_url"]}" alt="Error"></td>'
        html+= '</tr>'

    html+= '</table>'
    html += "</html>"

    send_email(subject="[Daily Briefing] My Morning Report", html=html)
