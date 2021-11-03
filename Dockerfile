FROM nikolaik/python-nodejs:python3.9-nodejs16
RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && git clone https://github.com/doellbarr/solidmusic solidmusic
WORKDIR /usr/local/solidmusic
COPY . /app
WORKDIR /app
RUN . venv/bin/activate \
    && pip3 install --no-cache-dir --upgrade --requirement requirements.txt
CMD ["python3", "main.py"]
