FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app


RUN addgroup --system python && adduser --system --group python


RUN pip install --no-cache-dir flask


COPY app/ .


RUN chown -R python:python /app


USER python


EXPOSE 5000

CMD ["python", "app.py"]