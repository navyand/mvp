from flask import Flask
from google.cloud import monitoring_v3
from google.auth import default
import os
import logging

app = Flask(__name__)

# Configura logging para que se vea en Cloud Logging
logging.basicConfig(level=logging.INFO)

# Detecta el ID del proyecto automáticamente
_, project = default()


def enviar_metricas():
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project}"

    series = monitoring_v3.TimeSeries()
    series.metric.type = "custom.googleapis.com/salus_demo/request_count"
    series.resource.type = "global"
    series.resource.labels["project_id"] = project
    series.points.add(
        value=monitoring_v3.TypedValue(int64_value=1),
        interval=monitoring_v3.TimeInterval(
            end_time={"seconds": int(monitoring_v3.types.Timestamp().seconds)},
        ),
    )

    client.create_time_series(name=project_name, time_series=[series])

    # Forzar salida para ver en logs
    logging.info("✅ Métrica enviada a Cloud Monitoring")


@app.route("/")
def hello():
    enviar_metricas()
    return "¡Salus MVP funcionando en la nube!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
