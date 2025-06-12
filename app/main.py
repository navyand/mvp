import os
import time
from flask import Flask
from google.cloud import monitoring_v3
from google.cloud.monitoring_v3 import types
from google.protobuf.timestamp_pb2 import Timestamp

app = Flask(__name__)
visit_count = 0  # Contador global de visitas


def enviar_metricas():
    global visit_count
    visit_count += 1

    # Cliente de Cloud Monitoring
    client = monitoring_v3.MetricServiceClient()

    # ID del proyecto desde variable de entorno
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

    if not project_id:
        raise EnvironmentError(
            "GOOGLE_CLOUD_PROJECT no está definido en las variables de entorno."
        )

    # Nombre del proyecto en formato requerido
    project_name = f"projects/{project_id}"

    series = monitoring_v3.TimeSeries()
    series.metric.type = "custom.googleapis.com/salus_mvp/visitas"
    series.resource.type = "global"
    series.resource.labels["project_id"] = project_id

    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10**9)

    interval = monitoring_v3.TimeInterval(
        end_time=Timestamp(seconds=seconds, nanos=nanos)
    )
    point = monitoring_v3.Point(
        {"interval": interval, "value": {"int64_value": visit_count}}
    )

    series.points.append(point)

    # Enviar la serie
    client.create_time_series(name=project_name, time_series=[series])


@app.route("/")
def hello():
    enviar_metricas()
    return f"¡Hola desde Salus MVP! Visitas: {visit_count}"
