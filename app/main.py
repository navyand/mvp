from flask import Flask
import os
import logging
from google.cloud import monitoring_v3
from google.cloud.monitoring_v3 import types
from google.auth import default
import time

app = Flask(__name__)

# Configura el logger para que se vean los logs en Cloud Logging
logging.basicConfig(level=logging.INFO)

# Autenticación implícita (GCP lo maneja en Cloud Run)
credentials, project_id = default()


def enviar_metricas():
    client = monitoring_v3.MetricServiceClient()

    series = monitoring_v3.TimeSeries()
    series.metric.type = "custom.googleapis.com/salus_mvp/solicitudes"
    series.resource.type = "global"
    series.resource.labels["project_id"] = project_id
    series.metric.labels["endpoint"] = "/"

    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10**9)

    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": seconds, "nanos": nanos},
        }
    )

    point = monitoring_v3.TypedValue(double_value=1.0)

    series.points.append(monitoring_v3.Point({"interval": interval, "value": point}))

    client.create_time_series(name=f"projects/{project_id}", time_series=[series])
    logging.info("✅ Métrica personalizada enviada a Cloud Monitoring")


@app.route("/")
def hello():
    enviar_metricas()
    return "¡Salus MVP funcionando en la nube y enviando métricas personalizadas!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
