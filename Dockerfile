# Dockerfile to create a Docker image for the Streamlit app
# Creates a layer from the python:3.8 Docker image
FROM python:3.8-slim

# Attach the package to a repository
LABEL org.opencontainers.image.source https://github.com/footballdaniel/algorithmicvalidation

# Copy all the files from the folders the Dockerfile is to the container root folder
COPY . .

# Install opencv for video/image manipulation
RUN apt-get install -y python-opencv

# Install the modules specified in the requirements.txt
RUN pip3 install -r requirements.txt

# The port on which a container listens for connections
EXPOSE 8501

# The command that run the app
CMD streamlit run validation.py

# To run locally https://maelfabien.github.io/project/Streamlit/#dockerfile
# docker run -p 8501:8501 algorithmicvalidation:latest