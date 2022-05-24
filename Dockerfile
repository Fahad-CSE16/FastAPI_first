FROM python:3.6-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

RUN apt-get update && apt-get install build-essential binutils libproj-dev gdal-bin curl -y
RUN pip3 install -U pip
ADD requirements.txt /app
RUN pip3 install -r requirements.txt && apt-get --purge autoremove build-essential -y
COPY api/ /app/api/
COPY ./api/routers.py /app/api/routers.py
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]