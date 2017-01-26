# Using official python runtime base image
FROM python

# Set the application directory
WORKDIR /app

# Install our requirements.txt
ADD requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copy our code from the current folder to /app inside the container
ADD . /app

# Make port 80 available for links and/or publish
EXPOSE 5000
EXPOSE 80

# ENVIRONMENT VARIABLE
ENV FLASK_APP app.py

# Define our command to be run when launching the container
CMD flask run --host=0.0.0.0