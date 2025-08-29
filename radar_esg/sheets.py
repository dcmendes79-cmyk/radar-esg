import os
import json
import gspread
from datetime import datetime
from google.oauth2.service_account import Credentials


REQUIRED_COLUMNS = [
"nome", "área", "público_alvo", "data", "local",
"edicoes_anteriores", "link_oficial", "fonte", "coletado_em"
]




def _client_from_env():
creds_json = os.getenv("GOOGLE_CREDENTIALS")
if not creds_json:
raise RuntimeError("GOOGLE_CREDENTIALS não encontrado nas variáveis de ambiente.")
info = json.loads(creds_json)
scopes = [
"https://www.googleapis.com/auth/spreadsheets",
"https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_info(info, scopes=scopes)
return gspread.authorize(creds)




def _ensure_header(ws):
existing = ws.row_values(1)
if existing == REQUIRED_COLUMNS:
return
if not existing:
ws.append_row(REQUIRED_COLUMNS)
else:
# Ajusta colunas se necessário (simples: reescreve header)
ws.delete_rows(1)
ws.insert_row(REQUIRED_COLUMNS, 1)




def open_events_sheet():
sheet_id = os.getenv("SHEET_ID")
if not sheet_id:
raise RuntimeError("SHEET_ID ausente nas variáveis de ambiente.")
gc = _client_from_env()
sh = gc.open_by_key(sheet_id)
try:
ws = sh.worksheet("events")
except gspread.WorksheetNotFound:
ws = sh.add_worksheet(title="events", rows=1000, cols=len(REQUIRED_COLUMNS)+2)
_ensure_header(ws)
return ws




def get_existing_links(ws):
# Assume link_oficial na coluna 7 (index humano). Vamos ler toda a planilha de uma vez.
data = ws.get_all_records()
return set((row.get("link_oficial") or "").strip() for row in data if row.get("link_oficial"))




def append_events(ws, rows):
if not rows:
return 0
ws.append_rows(rows, value_input_option="RAW")
return len(rows)




def to_row_dict(e):
now = datetime.utcnow().isoformat()
return {
"nome": e.get("nome", "").strip(),
"área": e.get("área", "ESG"),
"público_alvo": e.get("público_alvo", "Profissionais / Empresas / Acadêmicos"),
"data": e.get("data", ""),
"local": e.get("local", ""),
"edicoes_anteriores": e.get("edicoes_anteriores", ""),
"link_oficial": e.get("link_oficial", ""),
"fonte": e.get("fonte", ""),
"coletado_em": now,
}




def to_row_list(row_dict):
return [row_dict[c] for c in REQUIRED_COLUMNS]
