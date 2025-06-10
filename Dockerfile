FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install -y fonts-dejavu-core
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
