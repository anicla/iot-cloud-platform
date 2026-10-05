FROM debian:bookworm-slim
RUN apt-get update \
    && apt-get install -y --no-install-recommends mosquitto mosquitto-clients \
    && rm -rf /var/lib/apt/lists/*
COPY entrypoint.sh /usr/local/bin/mosquitto-entrypoint.sh
COPY code/mosquitto.conf /etc/mosquitto/mosquitto.conf
RUN chmod +x /usr/local/bin/mosquitto-entrypoint.sh
CMD ["/usr/local/bin/mosquitto-entrypoint.sh"]
