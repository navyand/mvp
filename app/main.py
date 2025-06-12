from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "¡Salus MVP funcionando en la nube!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

import os
from flask import Flask
from google.cloud import monitoring_v3
from google.auth import default
from datetime import datetime
import time

app = Flask(__name__)

# Configura el cliente de Monitoring
credentials, project_id = default()
client = monitoring_v3.MetricServiceClient(credentials=credentials)
project_name = f"projects/{project_id}"


# Función para enviar una métrica personalizada
def enviar_metricas():
    series = monitoring_v3.TimeSeries()
    series.metric.type = "custom.googleapis.com/salus/solicitudes_exitosas"
    series.resource.type = "global"

    # Punto de datos con valor 1 (una solicitud exitosa)
    point = series.points.add()
    point.value.int64_value = 1
    point.interval.end_time.seconds = int(time.time())
    point.interval.end_time.nanos = int((time.time() % 1) * 10**9)

    client.create_time_series(name=project_name, time_series=[series])


@app.route("/")
def hello():
    enviar_metricas()
    return "¡Salus MVP funcionando en la nube!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
