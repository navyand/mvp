from flask import Flask
import os
from google.cloud import monitoring_v3
import logging

app = Flask(__name__)


def enviar_metricas():
    logging.basicConfig(level=logging.INFO)
    print("⚙️ Ejecutando función enviar_metricas()")
    logging.info("⚙️ Ejecutando función enviar_metricas()")

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        logging.warning("❌ No se encontró GOOGLE_CLOUD_PROJECT")
        return

    try:
        client = monitoring_v3.MetricServiceClient()
        project_name = f"projects/{project_id}"

        series = monitoring_v3.TimeSeries()
        series.metric.type = "custom.googleapis.com/salus/mvp_availability"
        series.resource.type = "global"
        series.resource.labels["project_id"] = project_id

        point = monitoring_v3.Point()
        point.value.double_value = 1.0
        point.interval.end_time.GetCurrentTime()
        series.points = [point]

        logging.info("📤 Enviando métrica personalizada desde salus-mvp")
        client.create_time_series(name=project_name, time_series=[series])
        logging.info("✅ Métrica personalizada enviada correctamente.")
    except Exception as e:
        logging.error(f"❌ Error al enviar métrica: {e}")


@app.route("/")
def hello():
    enviar_metricas()
    return "¡Salus MVP funcionando en la nube!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
