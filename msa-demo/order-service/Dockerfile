FROM python:3.14-slim
WORKDIR /app
COPY requirements.txt .
COPY wheels /wheels
RUN pip install --no-index --find-links=/wheels fastapi uvicorn
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]