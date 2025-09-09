# base image
FROM python:3.10-slim

WORKDIR /home/site/wwwroot

RUN which pip && pip --version
# install dependencies 
COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# copy in the source code
COPY . .

# expose the port that turtle runs on
EXPOSE 80

# Set the Flask app environment variable to the correct path
ENV FLASK_APP="src/api.py"

# Start the Flask application
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "80"]