ffrom flask import Flask
import time
import logging
from google.cloud import monitoring_v3

app = Flask(__name__)

# Configura el logging para que los mensajes se vean en Cloud Logging
logging.basicConfig(level=logging.INFO)

# ID de tu proyecto en GCP
PROJECT_ID = "virtual-muse-460520-u9"

def enviar_metricas():
    logging.info("Enviando métrica personalizada desde salus-mvp")

    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{PROJECT_ID}"

    series = monitoring_v3.TimeSeries()
    series.metric.type = "custom.googleapis.com/salus/mvp_availability"
    series.resource.type = "global"
    series.resource.labels["project_id"] = PROJECT_ID

    # Punto de datos con valor 1 (disponibilidad OK)
    point = monitoring_v3.Point()
    point.value.double_value = 1.0
    now = time.time()
    point.interval.end_time.seconds = int(now)
    point.interval.end_time.nanos = int((now - int(now)) * 10**9)

    series.points = [point]

    # Envía la serie a Cloud Monitoring
    client.create_time_series(name=project_name, time_series=[series])
    logging.info("✅ Métrica personalizada enviada correctamente.")

@app.route("/")
def hello():
    enviar_metricas()
    return "¡Salus MVP funcionando en la nube!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
