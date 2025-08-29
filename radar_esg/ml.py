from .config import AREAS


# Classificação simples por palavras‑chave (MVP). Evoluímos para ML depois.
def classify_area(text: str) -> str:
if not text:
return "ESG"
t = text.lower()
scores = {area: 0 for area in AREAS}
for area, kws in AREAS.items():
for kw in kws:
if kw.lower() in t:
scores[area] += 1
# Empate → ESG como padrão
best = sorted(scores.items(), key=lambda x: (-x[1], x[0]))[0]
return best[0]
