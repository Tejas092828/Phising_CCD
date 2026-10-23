pipeline {
    agent any
    environment {
        // You must configure this credential ID in Jenkins later
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-id') 
        IMAGE_NAME = "tejas0909/phising-ccd"
        IMAGE_TAG = "${env.BUILD_ID}"
    }
    stages {
        stage('Checkout') {
            steps {
                // Jenkins pulls the latest code
                git branch: 'main', url: 'https://github.com/Tejas092828/Phising_CCD.git'
            }
        }
        stage('Build and Test') {
            steps {
                // Application is built and tests are run
                // Tip: If your project has no tests, use a syntax-check step
                sh 'echo "Running syntax check as a test..."'
                sh 'python -m py_compile app.py' 
            }
        }
        stage('Docker Build') {
            steps {
                // Docker image is created from your Dockerfile[cite: 1]
                sh "docker build -t ${IMAGE_NAME}:latest -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }
        stage('Push Image') {
            steps {
                // Image is published to Docker Hub or AWS ECR[cite: 1]
                sh "echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin"
                sh "docker push ${IMAGE_NAME}:latest"
                sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }
        stage('Minikube Deployment') {
            steps {
                // Kubernetes Deployment and Service are applied
                sh "kubectl apply -f k8s/deployment.yaml"
                sh "kubectl apply -f k8s/service.yaml"
                // Forces Kubernetes to use the newly pushed image
                sh "kubectl set image deployment/phising-app-deployment phising-app-container=${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }
        stage('Verification') {
            steps {
                // Pods, deployment and service checked
                sh "kubectl get deployments"
                sh "kubectl get pods"
                sh "kubectl get svc"
            }
        }
    }
}