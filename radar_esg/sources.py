import os
import requests
from datetime import datetime
from dateutil import parser


EVENTBRITE_TOKEN = os.getenv("EVENTBRITE_TOKEN")


class SourceError(Exception):
pass




def eventbrite_search(query: str, country: str, page_size: int = 50):
"""Busca eventos no Eventbrite usando o termo e país. Retorna lista de dicionários padronizados."""
if not EVENTBRITE_TOKEN:
raise SourceError("Falta EVENTBRITE_TOKEN nas variáveis de ambiente.")


url = "https://www.eventbriteapi.com/v3/events/search/"
params = {
"q": query,
"location.address": country,
"sort_by": "date",
"expand": "venue",
"page": 1,
"page_size": page_size,
}
headers = {"Authorization": f"Bearer {EVENTBRITE_TOKEN}"}


out = []
r = requests.get(url, params=params, headers=headers, timeout=30)
r.raise_for_status()
data = r.json()
events = data.get("events", [])


for e in events:
name = (e.get("name", {}) or {}).get("text") or "(sem título)"
link = e.get("url")
start = (e.get("start", {}) or {}).get("local")
dt = None
if start:
try:
dt = parser.parse(start)
except Exception:
dt = None
venue = e.get("venue") or {}
online = e.get("online_event", False)
if online:
local = "Online"
else:
pieces = [venue.get("name"), venue.get("address", {}).get("city"), venue.get("address", {}).get("country")]
local = ", ".join([p for p in pieces if p]) or country


out.append({
"nome": name.strip(),
"data": dt.isoformat() if dt else "",
"local": local,
"link_oficial": link,
"fonte": "Eventbrite",
})


return out
