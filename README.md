# Image Text Extractor

## Overview

This project consists of a Flask backend and a Streamlit frontend, designed to extract text from images on any given webpage. It uses OCR (Optical Character Recognition) via Tesseract to process images and extract text.

## Setup and Installation

### Requirements
- Python 3.6+
- Flask
- Requests
- BeautifulSoup4
- Pillow
- Pytesseract
- Pydantic
- Streamlit

## Here's an abstract ASCII representation of the directory tree for the repository:

```
image-text-extractor/
│
├── backend/
│   ├── app.py               # Flask application
│   ├── requirements.txt     # Python dependencies for Flask
│   └── Dockerfile-flask     # Dockerfile for Flask app
│
├── frontend/
│   ├── app.py               # Streamlit application
│   ├── requirements.txt     # Python dependencies for Streamlit
│   └── Dockerfile-streamlit # Dockerfile for Streamlit app
│
├── docker-compose.yml       # Docker Compose configuration file
└── README.md                # Project documentation
```

- The `backend` directory contains your Flask application along with its requirements and Dockerfile.
- The `frontend` directory includes the Streamlit application, its requirements, and Dockerfile.
- The `docker-compose.yml` file at the root of the project is used to orchestrate both the Flask and Streamlit applications. 
- The `README.md` provides an overview and instructions for the project.

# Installation

1. Install the required Python packages:
   ```bash
   pip install Flask requests BeautifulSoup4 pillow pytesseract pydantic streamlit
   ```

2. Clone this repository:
   ```bash
   git clone https://github.com/Cdaprod/image-text-extractor
   ```

3. Navigate into the project directory:
   ```bash
   cd image-text-extractor
   ```

## Running the Application

### Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Start the Flask app:
   ```bash
   python app.py
   ```
   This runs the backend on `localhost:5001`.

### Frontend

1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```
   This launches the Streamlit UI in your default web browser.

# Containerized with Docker

To containerize your Flask and Streamlit applications using Docker, you will need two Dockerfiles - one for each application - and a Docker Compose file to run them together. Here's how you can set them up:

### Dockerfile for Flask Backend (`Dockerfile-flask`):

```Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./backend /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5001 available to the world outside this container
EXPOSE 5001

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]
```

### Dockerfile for Streamlit Frontend (`Dockerfile-streamlit`):

```Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./frontend /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run app.py when the container launches
CMD ["streamlit", "run", "app.py"]
```

### Docker Compose File (`docker-compose.yml`):

```yaml
version: '3'
services:
  flask-backend:
    build: 
      context: .
      dockerfile: Dockerfile-flask
    ports:
      - "5001:5001"
  
  streamlit-frontend:
    build: 
      context: .
      dockerfile: Dockerfile-streamlit
    ports:
      - "8501:8501"
    depends_on:
      - flask-backend
```

### Steps to Run:

1. Place the `Dockerfile-flask` in your backend directory and the `Dockerfile-streamlit` in your frontend directory.
2. Place the `docker-compose.yml` file in the root directory of your project (where the backend and frontend directories are).
3. Run `docker-compose up` from the root directory. This will build and run both the Flask and Streamlit containers.

This setup will allow you to run both applications in separate Docker containers, with Streamlit interacting with the Flask backend as required.

---

## Usage

Enter the URL of the webpage containing images in the Streamlit UI. Click the "Extract Text" button to process the images and display the extracted text.

## License

This project is licensed under the [MIT License].