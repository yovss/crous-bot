FROM python:3.13-slim

# Force Python to print logs immediately to the Railway console
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

# Install your Python packages AND honcho
RUN pip install --no-cache-dir -r requirements.txt honcho

# Install Playwright browser and its Linux dependencies
RUN playwright install --with-deps chromium

COPY . .

# Start honcho, which will read the Procfile and start BOTH scripts
CMD ["honcho", "start"]