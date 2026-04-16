# 1. Use a lightweight Python base image
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy only the requirements file
COPY requirements.txt .

# 4. Install the libraries
RUN python -m pip install -r requirements.txt

# 5. Copy the rest of your application code
COPY . .

# 6. Create user and group for generting the log files
RUN addgroup --system appgroup && adduser --system --group appuser
RUN touch ddns-info.log && chown appuser:appgroup ddns-info.log
RUN touch ddns-error.log && chown appuser:appgroup ddns-error.log
COPY --chown=appuser:appgroup . .
USER appuser

# 7. Command to run your script
CMD ["python","DDNS-Updater.py"]