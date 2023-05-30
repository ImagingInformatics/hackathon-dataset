# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the code and configuration files into the container
COPY . /app

# Install the dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install the package inside the container
RUN pip install -e .

# Set up the shared volume and its subdirectories
VOLUME /app/data/inputs
VOLUME /app/data/output

# Set the entrypoint to run command-line commands on the shared volume
ENTRYPOINT ["siimhack"]

# Default command if no arguments are provided
CMD ["--help"]