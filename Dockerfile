FROM python:3.12.6
WORKDIR /app
COPY . /app/
RUN pip install -r requirements.txt
# Install ffmpeg using apt
RUN apt-get update && apt-get install -y ffmpeg && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/*
CMD python bot.py
