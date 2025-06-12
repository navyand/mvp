from flask import Flask
from google.cloud import monitoring_v3
import time

app = Flask(__name__)


def enviar_metricas():
    client = monitoring_v3.MetricServiceClient()
    # Obtener el ID del proyecto desde el cliente (sin depender de variables de entorno)
    project_id = client.project.split("/")[-1]
    project_name = f"projects/{project_id}"

    series = monitoring_v3.TimeSeries()
    series.metric.type = "custom.googleapis.com/salus_mvp/visitas"
    series.resource.type = "global"

    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10**9)

    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": seconds, "nanos": nanos},
            "start_time": {"seconds": seconds, "nanos": nanos},
        }
    )

    value = monitoring_v3.TypedValue(
        double_value=1.0
    )  # Siempre +1 visita por cada solicitud
    point = monitoring_v3.Point({"interval": interval, "value": value})
    series.points.append(point)

    print("✅ Enviando métrica personalizada: +1 visita")

    client.create_time_series(name=project_name, time_series=[series])


@app.route("/")
def hello():
    enviar_metricas()
    return "¡Salus MVP funcionando y enviando métricas personalizadas desde Cloud Run!"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
