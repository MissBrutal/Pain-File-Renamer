FROM python:3.10
WORKDIR /app
COPY . /app/
COPY hold.py
RUN pip install -r requirements.txt
# Install ffmpeg using apt
RUN apt update && apt install -y ffmpeg
CMD python bot.py && python hold.py
