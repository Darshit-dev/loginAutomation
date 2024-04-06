# Use the official Python 3.9 image as the base image
FROM python:3.9-slim

# Install Chrome and Chromedriver dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    gnupg \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libxrender1 \
    libxcomposite1 \
    libasound2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Download and install Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable

# Download the latest Chromedriver
RUN wget -q https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.86/linux64/chromedriver-linux64.zip -O /tmp/chromedriver_linux64.zip  && ls -l /tmp/chromedriver_linux64.zip

# Extract Chromedriver and move to /usr/local/bin (verify download first)
RUN if [ -f /tmp/chromedriver_linux64.zip ]; then \
    unzip /tmp/chromedriver_linux64.zip -d /tmp && chmod +x /tmp/chromedriver-linux64/chromedriver && mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && rm /tmp/chromedriver_linux64.zip; \
    fi

# Install Selenium
RUN pip install selenium

# Copy the Lambda function code into the container
COPY lambda_function.py /var/task/lambda_function.py

# Set the working directory
WORKDIR /var/task

# Command to run the Lambda function
CMD ["python", "lambda_function.py"]
