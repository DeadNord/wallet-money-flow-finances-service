# pull official base image
FROM python:3.11.4-slim-buster


# Set the working directory inside the container
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy the Python dependencies file to the container and install them.
RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project's code into the container
COPY . .

CMD ["python", "./finances_service/manage.py", "runserver", "0.0.0.0:3003"]