FROM python:3.7

WORKDIR /app
RUN apt-get update
RUN apt-get install -y iceweasel
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz && \
tar -xvzf geckodriver* && \
chmod +x geckodriver && \
mv geckodriver /usr/local/bin/

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app
CMD python main_flow.py