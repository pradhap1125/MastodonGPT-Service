# Use a Linux-based Python image
FROM python:3.10-slim

WORKDIR /app

COPY dist/mastodongpt-0.1.0-py3-none-any.whl /app/mastodongpt-0.1.0-py3-none-any.whl

CMD pip install --no-cache-dir /app/mastodongpt-0.1.0-py3-none-any.whl

EXPOSE 5000

CMD ["waitress-serve", "--port=", "5000", "mastodongpt.app:app"]