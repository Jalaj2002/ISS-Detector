import time

import requests
import datetime
import smtplib

My_lat = 26.449923  # Your location latitude and longitude
My_lng = 80.331871
My_email = "jalajsrivastav1728@gmail.com"
My_password = "xxxxxxx"


# _____________________ Get the current position of International Space Station ____________________
def is_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()

    data = response.json()
    print(data)
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    print(iss_latitude)
    print(iss_longitude)
    # iss_position = (iss_longitude, iss_latitude)
    if My_lat - 5 <= iss_latitude <= My_lat + 5 and My_lng - 5 <= iss_longitude <= My_lng + 5:
        return True


# _________________________ Get the sunrise and Sunset timings of your current location ____________________

def is_night():
    parameters = {
        "lat": My_lat,
        "lng": My_lng,
        "formatted": 0
    }

    response_2 = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response_2.raise_for_status()
    timings = response_2.json()
    print(timings)

    sunrise = timings["results"]["sunrise"].replace("T", " ").split("+")[0] + ".0000"
    sunrise_dt = datetime.datetime.strptime(sunrise, '%Y-%m-%d %H:%M:%S.%f')
    sunrise_time = sunrise_dt + datetime.timedelta(hours=5, minutes=30)
    print(sunrise_time)
    sunrise_hour = sunrise_time.hour

    sunset = timings["results"]["sunset"].replace("T", " ").split("+")[0] + ".0000"
    sunset_dt = datetime.datetime.strptime(sunset, '%Y-%m-%d %H:%M:%S.%f')
    sunset_time = sunset_dt + datetime.timedelta(hours=5, minutes=30)
    print(sunset_time)
    sunset_hour = sunset_time.hour

    time_now_hour = datetime.datetime.now().hour
    if sunset_hour <= time_now_hour or time_now_hour <= sunrise_hour:
        return True


while True:
    time.sleep(60)
    if is_night() and is_overhead():
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(user=My_email, password=My_password)
        connection.sendmail(from_addr=My_email, to_addrs=My_email,
                            msg="Subject:Hey! Look Up👆\n\n The International Space "
                                "Station is above you in the sky. ")
