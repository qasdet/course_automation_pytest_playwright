FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libxss1 libxcomposite1 libxrandr2 libgbm1 libasound2 libpangocairo-1.0-0 libgtk-3-0 && \
    pip install -U pip && pip install -r requirements.txt && \
    playwright install --with-deps

CMD ["bash"]
