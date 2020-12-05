import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 32.291611
MY_LONG = -110.838051
MY_EMAIL = "novusterra6@gmail.com"
MY_PASSWORD = "pflyers88"
EMAIL_SERVER = "smtp.gmail.com"
PORT = 587

def is_iss_overhead():
    """Determines if the ISS is overhead ± 5 degrees returns true."""
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # If position is within +5 or -5 degrees of the ISS position.
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True

def is_night():
    """Determines if current time is night time returns true."""
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now_hour = datetime.now().hour
    
    if time_now_hour >= sunset or time_now_hour <= sunrise:
        return True

while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        with smtplib.SMTP(EMAIL_SERVER, PORT) as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg="Subject: ISS is Overhead👆\n\nThe ISS is above you in space."
            )



