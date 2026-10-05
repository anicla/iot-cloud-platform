FROM python:3.12-slim
COPY ./code /etc/usr/src/app
WORKDIR /etc/usr/src/app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "IoTContainerSimulator.py"]
