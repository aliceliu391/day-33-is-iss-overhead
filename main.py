import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 43.653225
MY_LONG = -79.383186

my_email = "your_email@gmail.com"
password = "your_password"


def iss_is_overhead():
    """Checks if the ISS is within +-5 of your latitude and longitude"""

    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    lat_difference = abs(MY_LAT - iss_latitude)
    long_difference = abs(MY_LONG - iss_longitude)

    if lat_difference <= 5 and long_difference <= 5:
        return True
    else:
        return False


parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }


def is_dark():
    """Checks if the sky is dark"""

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now <= sunrise or time_now >= sunset:
        return True


while True:
    if is_dark() and iss_is_overhead():
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email,
                                to_addrs=my_email,
                                msg="Subject: Look up !! <3\n\nThe ISS is overhead, you don't want to miss this.")

    time.sleep(60)
