from flask import Flask
import os
from google.cloud import monitoring_v3
from google.cloud.monitoring_v3 import types
from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime
import time

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)


app = Flask(__name__)
contador_visitas = 0

def enviar_metricas():
    global contador_visitas
    contador_visitas += 1  # Incrementa contador

    # Verifica si está definida la variable de entorno
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "virtual-muse-460520-u9")
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    series = monitoring_v3.TimeSeries()
    series.metric.type = "custom.googleapis.com/solicitudes"
    series.resource.type = "global"

    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10**9)

    interval = monitoring_v3.TimeInterval(
        end_time=Timestamp(seconds=seconds, nanos=nanos)
    )
    point = monitoring_v3.TypedValue(int64_value=contador_visitas)
    series.points.append(monitoring_v3.Point(interval=interval, value=point))

    series.resource.labels["project_id"] = project_id

    client.create_time_series(name=project_name, time_series=[series])
    print(f"[INFO] Métrica enviada. Contador actual: {contador_visitas}")

@app.route("/")
def hello():
    enviar_metricas()
    return f"¡Hola desde Salus! Visitas: {contador_visitas}"
