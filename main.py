import os
from datetime import datetime
from radar_esg.config import QUERIES, COUNTRIES, DEFAULT_AUDIENCE
from radar_esg.sources import eventbrite_search
from radar_esg.ml import classify_area
from radar_esg.sheets import open_events_sheet, get_existing_links, append_events, to_row_dict, to_row_list
from radar_esg.emailer import send_email




def run():
sheet_link = f"https://docs.google.com/spreadsheets/d/{os.getenv('SHEET_ID')}/edit#gid=0"
all_events = []


for q in QUERIES:
for country in COUNTRIES:
try:
events = eventbrite_search(q, country)
all_events.extend(events)
except Exception as e:
print(f"Falha {q}/{country}: {e}")


# Enriquecimento (classificação + campos faltantes)
enriched = []
for e in all_events:
area = classify_area((e.get("nome") or "") + " " + (e.get("fonte") or ""))
e["área"] = area
e["público_alvo"] = DEFAULT_AUDIENCE
e.setdefault("edicoes_anteriores", "")
enriched.append(e)


ws = open_events_sheet()
existing =
