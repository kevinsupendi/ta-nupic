from prometheus_client import start_http_server, Gauge
from detectors.base import detectDataSet
from detectors.numenta.numenta_detector import NumentaDetector
import time
import requests
import datetime

# Create a metric to track time spent and requests made.
g1 = Gauge('anomaly_score', 'Anomaly Likelihood')
g2 = Gauge('raw_score', 'Anomaly Raw Score')

def getDataRow():
    # debug local
    # prometheus_url = "http://35.240.222.157:30070/api/v1/query"
    # production
    prometheus_url = "http://prometheus-k8s.monitoring.svc:9090/api/v1/query"
    expr = "sum by (container_name) (rate(container_cpu_usage_seconds_total{job=\"kubelet\", image!=\"\",container_name=\"php-redis\"}[1m]))"
    r = requests.get(prometheus_url + "?query=" + expr)
    result = r.json()
    value = result['data']['result'][0]['value']
    t = datetime.datetime.fromtimestamp(value[0])
    str_time = t.strftime('%Y-%m-%d %H:%M:%S')
    return {"timestamp":datetime.datetime.strptime(str_time, '%Y-%m-%d %H:%M:%S'), "value":float(value[1])}


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    numenta = NumentaDetector()
    numenta.initialize()
    while True:
        dataRow = getDataRow()
        print dataRow
        args = (
            numenta,
            dataRow
        )
        result = detectDataSet(args)
        print result
        g1.set(result[0])
        g2.set(result[1])
        time.sleep(10)
