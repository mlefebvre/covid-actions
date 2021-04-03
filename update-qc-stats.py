import requests


def parse_history(j):
    cases = int(j["C"])
    recovered = int(j["R"])
    dead = int(j["D"])
    active = cases - recovered - dead
    hospital = int(j["H"])
    icu = int(j["I"])
    vaccines = int(j["V"])

    return {
        "cases": cases,
        "active": active,
        "recovered": recovered,
        "dead": dead,
        "hospital": hospital,
        "icu": icu,
        "vaccines": vaccines,
    }


response = requests.get("https://kustom.radio-canada.ca/covid-19/canada_quebec")
history = response.json()[0]["History"]

today = parse_history(history[0])
yesterday = parse_history(history[1])
day_before_yesterday = parse_history(history[2])

if today != yesterday:
    with open("daily_stats.txt", "w", encoding="UTF-8") as f:
        for key, value in today.items():
            diff = value - yesterday[key]
            previous_diff = yesterday[key] - day_before_yesterday[key]

            emoji = ""
            if diff > previous_diff:
                emoji = ":wau:"
            elif diff < previous_diff:
                emoji = ":wau_down:"

            line = f"{key}: {value} ({diff})"
            print(f"::set-output name={key}::{value} ({diff:+}) {emoji}")
            f.write(f"{key}: {value} ({diff})\n")
