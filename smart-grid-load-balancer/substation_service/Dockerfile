FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install flask requests prometheus_client
CMD ["python", "main.py"]
