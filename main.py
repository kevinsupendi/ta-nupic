from prometheus_client import start_http_server, Gauge
from detectors.base import detectDataSet
from detectors.numenta.numenta_detector import NumentaDetector
from collections import deque
import time
import requests
import datetime
import os
import numpy as np

# Create a metric to track time spent and requests made.
gauge1 = os.environ.get('GAUGE1')
gauge2 = os.environ.get('GAUGE2')
gauge3 = os.environ.get('GAUGE3')
g1 = Gauge(gauge1, 'Anomaly Likelihood')
g2 = Gauge(gauge2, 'Anomaly Raw Score')
g3 = Gauge(gauge3, 'Multiple Anomaly Likelihood')


expr = os.environ.get('EXPR')#"sum by (container_name) (rate(container_cpu_usage_seconds_total{job=\"kubelet\", image!=\"\",container_name=\"php-redis\"}[1m]))"
expr2 = os.environ.get('EXPR2')

def getDataRow(expression):
    # debug local
    # prometheus_url = "http://35.240.222.157:30070/api/v1/query"
    # production
    prometheus_url = "http://prometheus-k8s.monitoring.svc:9090/api/v1/query"
    r = requests.get(prometheus_url + "?query=" + expression)
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
    numenta.initialize(os.environ.get('INPUT_MIN1'), os.environ.get('INPUT_MAX1'))
    numenta2 = NumentaDetector()
    numenta2.initialize(os.environ.get('INPUT_MIN2'), os.environ.get('INPUT_MAX2'))
    d = deque(maxlen=1000)
    d2 = deque(maxlen=1000)
    print "Debug:"
    print "Expression " + os.environ.get('EXPR')
    print "Expression 2 " + os.environ.get('EXPR2')
    print "Gauge 1 " + os.environ.get('GAUGE1')
    print "Gauge 2 " + os.environ.get('GAUGE2')
    print "Gauge 3 " + os.environ.get('GAUGE3')
    print "Input Min " + os.environ.get('INPUT_MIN1')
    print "Input Max " + os.environ.get('INPUT_MAX1')
    print "Input Min 2 " + os.environ.get('INPUT_MIN2')
    print "Input Max 2 " + os.environ.get('INPUT_MAX2')
    while True:
        dataRow = getDataRow(expr)
        dataRow2 = getDataRow(expr2)
        print dataRow
        args = (
            numenta,
            dataRow
        )
        args2 = (
            numenta2,
            dataRow2
        )
        result = detectDataSet(args)
        print result
        result2 = detectDataSet(args2)
        g1.set(result[0])
        g2.set(result[1])

        d.append(1 - result[0])
        d2.append(1 - result2[0])
        filter_length = 8
        sigma = 2
        mid = filter_length / 2
        gaussian = [(1 / (sigma * np.sqrt(2 * np.pi))) * (1 / (np.exp((i ** 2) / (2 * sigma ** 2)))) for i in
                  range(-mid, mid + 1)]
        gaussian[:] = [x / sum(gaussian) for x in gaussian]
        final = 1 - (np.convolve(gaussian, d, 'valid'))[-1] * (np.convolve(gaussian, d2, 'valid'))[-1]
        g3.set(final)
        time.sleep(10)
