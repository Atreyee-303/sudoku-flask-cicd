# Sudoku Flask CI/CD Project

## 1. Project Overview
This project is a web-based Sudoku game developed using Python and Flask. It demonstrates a CI/CD workflow using Jenkins, Docker, Docker Hub, and Kubernetes with Minikube.

## 2. Technologies Used
- Python and Flask
- Pytest for automated testing
- Git and GitHub for version control
- Jenkins for CI/CD
- Docker for containerization
- Docker Hub for image storage
- Kubernetes and Minikube for deployment

## 3. Application Features
- Generates Sudoku puzzles.
- Allows users to enter and validate moves.
- Provides a limited number of lives.
- Supports starting a new game.
- Includes automated unit tests.

## 4. CI/CD Pipeline
The Jenkins pipeline performs the following stages:

1. **Checkout:** Retrieves the source code from GitHub.
2. **Install Dependencies and Test:** Installs Python dependencies and runs automated tests.
3. **Build Docker Image:** Builds the application Docker image.
4. **Push to Docker Hub:** Authenticates using Jenkins credentials and pushes the image to Docker Hub.

## 5. Containerization
The Dockerfile packages the Flask application, templates, dependencies, and tests into a Docker image.

Docker image: `atreyeek/sudoku-flask-cicd:v1`

## 6. Kubernetes Deployment
The application is deployed on Minikube using Kubernetes Deployment and Service manifests located in the `k8s/` directory.

- Deployment: `sudoku-flask`
- Replicas: 2
- Service: `sudoku-flask-service`
- Service type: NodePort
- NodePort: 30080

## 7. Testing and Verification
Automated tests are executed through Pytest in the Jenkins pipeline. The Kubernetes deployment was verified using `kubectl rollout status deployment/sudoku-flask`.

## 8. Project Links
- GitHub Repository: [Insert your GitHub repository URL]
- Docker Hub Repository: https://hub.docker.com/r/atreyeek/sudoku-flask-cicd

## 9. Conclusion
This project demonstrates automated testing, Docker image creation and publishing, and Kubernetes deployment of a Flask application. The current Jenkins pipeline automates testing, image building, and image publishing. Kubernetes deployment and verification are performed separately using Minikube.
