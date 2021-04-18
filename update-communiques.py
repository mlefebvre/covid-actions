import json
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
import os

communiques_url = "https://www.msss.gouv.qc.ca/ministere/salle-de-presse/communiques/"
response = requests.get(communiques_url)
soup = BeautifulSoup(response.text, features="html.parser")
tableau_comm = soup.find(id="tableauComm")
communiques = tableau_comm.find_all("a")

communiques_path = "communiques.json"
saved_communiques = {}
if os.path.exists(communiques_path):
    with open(communiques_path, "r") as f:
        saved_communiques = json.load(f)

new_communiques = {}
output = []

for communique in communiques:
    url = urljoin(communiques_url, communique.attrs["href"])
    title = communique.text.strip()
    if not title.startswith("Pandémie de la COVID-19") or "vaccination" not in title.lower():
        continue

    if url in saved_communiques:
        continue

    new_communiques[url] = title
    output.append(f"<{url}|{title}>")


output = ",".join(output).replace("%", "%25")
print(f"::set-output name=communiques::{output}")

saved_communiques.update(new_communiques)
with open(communiques_path, "w") as f:
    json.dump(saved_communiques, f, indent=4)

