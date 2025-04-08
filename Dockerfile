FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .


# CMD ["python", "run.py"]
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]


