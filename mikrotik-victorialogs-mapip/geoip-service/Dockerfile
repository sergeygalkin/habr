FROM python:3.12.9-alpine3.21

RUN pip install flask geoip2 requests

COPY geoip-service.py /usr/local/bin/

CMD ["python", "/usr/local/bin/geoip-service.py"]
