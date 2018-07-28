FROM python:2.7

COPY . /

ENV PYTHONUNBUFFERED=1
RUN pip2 install prometheus_client
RUN pip2 install nupic
RUN pip2 install numpy
RUN pip2 install requests

EXPOSE 8000

CMD ["python2", "main.py"]