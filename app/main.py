from flask import Flask
import os
import time
from google.cloud import monitoring_v3
from google.cloud.monitoring_v3.types import Point, TimeInterval, TypedValue, TimeSeries

app = Flask(__name__)


def enviar_metricas():
    client = monitoring_v3.MetricServiceClient()
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    project_name = f"projects/{project_id}"

    series = TimeSeries()
    series.metric.type = "custom.googleapis.com/salus_mvp/visitas"
    series.resource.type = "global"

    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10**9)

    interval = TimeInterval(
        {
            "end_time": {"seconds": seconds, "nanos": nanos},
            "start_time": {
                "seconds": seconds,
                "nanos": nanos,
            },  # Para DELTA está bien si es igual
        }
    )

    # Enviar +1 por cada visita
    value = TypedValue(double_value=1.0)
    point = Point({"interval": interval, "value": value})
    series.points.append(point)

    # Imprimir log para confirmar
    print("✅ Enviando métrica personalizada: +1 visita")

    client.create_time_series(name=project_name, time_series=[series])


@app.route("/")
def hello():
    enviar_metricas()
    return "¡Salus MVP funcionando en la nube y enviando métricas personalizadas!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
