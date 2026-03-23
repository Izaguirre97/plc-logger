import snap7
import time
import os
from datetime import datetime

PLC_IP = "192.168.120.55"
RACK = 0
SLOT = 0
LOG_FILE = r"C:\logs_plc\errores_plc.txt"
INTERVALO_SEGUNDOS = 600

os.makedirs(r"C:\logs_plc", exist_ok=True)

eventos_vistos = set()

def escribir_log(mensaje):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(mensaje + "\n")

def leer_buffer():
    try:
        plc = snap7.client.Client()
        plc.connect(PLC_IP, RACK, SLOT)
        diag = plc.read_sz_info()
        nuevos = 0
        for e in diag:
            eid = (e.EventID, e.TimeStamp)
            if eid not in eventos_vistos:
                eventos_vistos.add(eid)
                ts = datetime.fromtimestamp(e.TimeStamp).strftime("%Y-%m-%d %H:%M:%S")
                escribir_log(f"[{ts}] EventID: {hex(e.EventID)} | Info1: {e.Info1} | Info2: {e.Info2}")
                nuevos += 1
        plc.disconnect()
        if nuevos > 0:
            escribir_log(f"--- {nuevos} nuevo(s) el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
    except Exception as ex:
        escribir_log(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ERROR: {ex}")

escribir_log(f"\n{'='*60}")
escribir_log(f"Logger arrancado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
escribir_log(f"{'='*60}")

while True:
    leer_buffer()
    time.sleep(INTERVALO_SEGUNDOS)
