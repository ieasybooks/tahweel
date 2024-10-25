# Use the official Python 3.13 Slim image as the base image
FROM python:3.13-slim

# Set the working directory to /tahweel
WORKDIR /tahweel

# Install system dependencies
RUN apt-get update && \
    apt-get install -y poppler-utils && \
    rm -rf /var/lib/apt/lists/*

# Install tahweel
RUN pip install tahweel

# Set the entrypoint to run the installed binary in /tahweel
# Example: docker run -it --rm -v "$PWD:/tahweel" tahweel ...
ENTRYPOINT ["tahweel"]
