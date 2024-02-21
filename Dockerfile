# syntax=docker/dockerfile:1

# Build stage
FROM python:3.12.2-slim-bookworm as builder

ENV GECKODRIVER_URL="https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz"

#ARG PUID=1000
#ARG PGUID=1000

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

ENV DEBIAN_FRONTEND="noninteractive"

WORKDIR /

# Create a non-root user
#RUN addgroup --gid $PGUID brokerr-group && \
#    adduser --disabled-password --gecos '' --uid $PUID --gid $PGUID brokerr-user && \
    # install packages

RUN apt-get update && apt-get install -y \
    firefox-esr wget python3-pip supervisor redis-server redis-tools \
    && wget $GECKODRIVER_URL -O geckodriver-v0.34.0-linux64.tar.gz && \
    tar -xzf geckodriver-v0.34.0-linux64.tar.gz -C /usr/bin && \
    chmod +x /usr/bin/geckodriver && \
    rm -f geckodriver-v0.34.0-linux64.tar.gz \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get purge -y --auto-remove wget \
    && export PATH=$PATH:/usr/bin/

# Copy the supervisor configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
# Copy the redis configuration file
COPY redis.conf /etc/redis/redis.conf
    
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    pip install --no-build-isolation -r requirements.txt

# TODO: Get a slimmer build working with multi-stage build
# Final stage
# FROM python:3.12.2-slim

# COPY --from=builder /usr/local/lib/python3.12 /usr/local/lib/python3.12
# COPY --from=builder /usr/bin/geckodriver /usr/bin/geckodriver
# COPY --from=builder /usr/lib/firefox-esr /usr/lib/firefox-esr
# COPY --from=builder /usr/bin/firefox /usr/bin/firefox
# COPY --from=builder /usr/bin/firefox-esr /usr/bin/firefox-esr

COPY brokerr /brokerr

WORKDIR /brokerr

EXPOSE 6363

# Switch to the specified user
#USER myuser:mygroup

CMD ["supervisord", "--nodaemon", "--configuration", "/etc/supervisor/supervisord.conf"]