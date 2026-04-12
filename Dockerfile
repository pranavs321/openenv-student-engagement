FROM python:3.10-slim

# Force unbuffered stdout so the validator gets logs instantly
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 7860

CMD ["python", "app.py"]
