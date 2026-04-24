FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY app.py /app/app.py

EXPOSE 8080

CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]