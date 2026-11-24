FROM python:3.14-slim
WORKDIR /app
COPY wheels /wheels
RUN pip install --no-index --find-links=/wheels fastapi uvicorn strawberry-graphql httpx
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
