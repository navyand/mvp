from flask import Flask
import os
from google.cloud import monitoring_v3
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


def enviar_metricas():
    logging.info("⚙️ Ejecutando función enviar_metricas()")

    client = monitoring_v3.MetricServiceClient()
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    project_name = f"projects/{project_id}"

    series = monitoring_v3.TimeSeries()
    series.metric.type = "custom.googleapis.com/salus/mvp_availability"
    series.resource.type = "global"
    series.resource.labels["project_id"] = project_id
    series.metric.labels["version"] = "v1"

    now = monitoring_v3.types.TimeInterval()
    from google.protobuf.timestamp_pb2 import Timestamp
    import time

    now.end_time.seconds = int(time.time())
    now.end_time.nanos = 0

    point = monitoring_v3.types.Point()
    point.interval = now
    point.value.double_value = 1.0  # disponibilidad 100%

    series.points = [point]
    client.create_time_series(name=project_name, time_series=[series])

    logging.info("📤 Enviando métrica personalizada desde salus-mvp")
    logging.info("✅ Métrica personalizada enviada correctamente.")


@app.route("/")
def hello():
    enviar_metricas()
    return "¡Salus MVP funcionando en la nube!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
