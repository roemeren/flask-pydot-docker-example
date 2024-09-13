# Flask Network Graph Visualization App

## Overview

This application is a Flask-based web service that allows users to upload CSV files containing network data. The app processes the CSV to generate network graphs and provides a downloadable PNG file for each network group. The entire application is dockerized and deployed using Render, with automatic deployment set up via GitHub Actions.

## Features

- **Upload CSV File**: Users can upload a CSV file with network data.
- **Generate Network Graph**: The app processes the CSV file and generates network graphs.
- **Download Graphs**: Users can download the generated graphs as PNG files.
- **Automatic Deployment**: Deployed on Render with automated updates via GitHub Actions.

## Steps to Create and Deploy the App

### 1. Application Development

1. **Create the Flask App**: 
   - Built a Flask application to handle file uploads, generate network graphs using Graphviz and pydot, and serve the graphs as downloadable files.
   - Utilized HTML forms for file uploads and download links.

2. **Dockerize the App**:
   - Created a Dockerfile to containerize the application, ensuring all dependencies and Graphviz are included.

3. **Local Testing**:
   - Tested the application locally in Docker to ensure it runs as expected.

### 2. GitHub Actions Setup

1. **Create GitHub Actions Workflow**:
   - Set up a GitHub Actions workflow to automatically deploy the app to Render when a tag is pushed to the repository.

2. **Configure Secrets**:
   - Added Render service ID as a GitHub secret for secure deployment.

### 3. Deploy on Render

1. **Configure Render**:
   - Set up a new Web Service on Render, pointed to the repository with the Dockerfile in the appropriate directory.

2. **Deploy the App**:
   - Deployed the app, ensuring that it is publicly accessible at the provided URL.

## Running the App Locally

To run the app locally:

1. **Build and Run Docker Container** (make sure that Docker is installed):
   ```bash
   docker build -t flask-graph-app .
   docker run -p 5000:5000 flask-graph-app
   ```

2. **Access the App**:
Open `http://localhost:5000` in your web browser.
