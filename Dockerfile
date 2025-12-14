FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY scanmyfiles.py .

EXPOSE 8000

ENV MCP_HOST=0.0.0.0
ENV MCP_PORT=8000
ENV SCAN_SERVICE_URL=""


CMD ["python", "scanmyfiles.py"]