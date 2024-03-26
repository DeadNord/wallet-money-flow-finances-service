# Use the official Python image as the base image
FROM python:3.9

# Allow passing the API port as a build argument, default to 8000 if not provided
ARG API_PORT=8000
# Set the API_PORT environment variable to match the build argument
ENV API_PORT=${API_PORT}

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the Python dependencies file to the container and install them.
# This ensures that the dependencies are cached and only need to be reinstalled if they change.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project's code into the container
COPY . .

# Make the service's port available outside the container
EXPOSE $API_PORT

# Define the default command to run the Django development server on the specified port
# The port number is taken from the API_PORT environment variable
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:${API_PORT}"]
