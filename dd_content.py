import pandas as pd
import csv
import random
import json
import config
from sqlalchemy import create_engine
from urllib import request
from datetime import datetime


engine = create_engine(
    f"postgresql://postgres:huperetes@localhost/dailydigest"
)  # connect to the postgresql database


"""
Retrieve random verse from database
"""


def get_verse(verses_file=f"{config.temp}/verses.csv"):
    df = pd.read_sql(
        "SELECT reference, verse FROM verses;",
        con=engine,
        index_col="reference",
    )
    df.to_csv(f"{config.temp}/verses.csv")

    try:
        with open(verses_file) as csvfile:
            verses = [
                {"reference": line[0], "verse": line[1]} for line in csv.reader(csvfile)
            ]
            verses.pop(0)

    except Exception as e:
        verses = [
            {
                "reference": "Matthew 28:10",
                "verse": "And behold, I am with you always, to the end of the age.",
            }
        ]

    return random.choice(verses)


"""
Retrieve the current weather forecast from OpenWeatherMap.
"""


def get_weather_forecast(
    coords={"lat": -1.286389, "lon": 36.817223}
):  # default location at Nairobi
    try:
        api_key = "3d3f14b950006ba1a30d0afde4cfa6b3"
        url = f'https://api.openweathermap.org/data/2.5/forecast?lat={coords["lat"]}&lon={coords["lon"]}&appid={api_key}&units=metric'
        data = json.load(request.urlopen(url))

        forecast = {
            "city": data["city"]["name"],
            "country": data["city"]["country"],
            "periods": list(),
        }

        for period in data["list"][0:9]:
            forecast["periods"].append(
                {
                    "timestamp": datetime.fromtimestamp(period["dt"]),
                    "temp": round(period["main"]["temp"]),
                    "description": period["weather"][0]["description"].title(),
                    "icon": f'http://openweathermap.org/img/wn/{period["weather"][0]["icon"]}.png',
                }
            )

        return forecast

    except Exception as e:
        print(e)


"""
Retrieve the day's devotions from database
"""


def get_devotion(devotions_file=f"{config.temp}/devotions.csv"):
    df = pd.read_sql(
        "SELECT readings FROM devotions;",
        con=engine,
        columns=None,
    )
    df.to_csv(f"{config.temp}/devotions.csv")

    try:
        with open(devotions_file) as csvfile:

            for line in csv.reader(csvfile):
                devotions = {"weekday": line[0], "readings": line[1]}
                if devotions["weekday"] == datetime.today().strftime("%A"):
                    break
    except Exception as e:
        print(e)

    return devotions


"""
Retrieve the summary extract for a random Wikipedia article.
"""


def get_wikipedia_article():
    try:
        data = json.load(
            request.urlopen("https://en.wikipedia.org/api/rest_v1/page/random/summary")
        )
        return {
            "title": data["title"],
            "extract": data["extract"],
            "url": data["content_urls"]["desktop"]["page"],
        }

    except Exception as e:
        print(e)


def test_module():
    # TODO: test get_random_verse()
    print("\nTesting verse generation...")

    verse = get_verse()
    print(f' - Random verse is "{verse["verse"]}" - {verse["reference"]}')

    # TODO: test get_weather_forecast()
    print("\nTesting weather forecast retrieval...")

    forecast = get_weather_forecast()
    if forecast:
        print(f'\nWeather forecast for {forecast["city"]}, {forecast["country"]} is...')
        for period in forecast["periods"]:
            print(
                f' - {period["timestamp"]} | {period["temp"]}°C | {period["description"]}'
            )

    # TODO: test get_devotion()
    print("\nTesting lesson generation...")

    devotions = get_devotion()
    print(
        f"{devotions['weekday']}'s devotions\n-------‐---------------------\n{devotions['readings']}"
    )

    # TODO: test get_wikipedia_article
    print("\nTesting random Wikipedia article retrieval...")

    article = get_wikipedia_article()
    if article:
        print(f'\n{article["title"]}\n<{article["url"]}>\n{article["extract"]}')


if __name__ == "__main__":
    test_module()
