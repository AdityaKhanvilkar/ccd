pipeline {
    agent any

    environment {
        DOCKER_USER = 'adityakhanvilkar'
        IMAGE_NAME  = 'cca-studentapp'
        IMAGE_TAG   = "${env.BUILD_NUMBER}"
        REGISTRY    = "docker.io/${DOCKER_USER}/${IMAGE_NAME}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build and Test') {
            steps {
                sh 'python3 -m py_compile app.py'
            }
        }

        stage('Docker Build') {
            steps {
                sh "docker build -t ${REGISTRY}:${IMAGE_TAG} ."
                sh "docker tag ${REGISTRY}:${IMAGE_TAG} ${REGISTRY}:latest"
            }
        }

        stage('Push Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
                    sh 'echo $DH_PASS | docker login -u $DH_USER --password-stdin'
                    sh "docker push ${REGISTRY}:${IMAGE_TAG}"
                    sh "docker push ${REGISTRY}:latest"
                }
            }
        }

        stage('Minikube Deployment') {
            steps {
                sh 'kubectl apply -f k8s/deployment.yaml'
                sh 'kubectl apply -f k8s/service.yaml'
                sh "kubectl set image deployment/studentapp-deployment studentapp=${REGISTRY}:${IMAGE_TAG}"
                sh 'kubectl rollout status deployment/studentapp-deployment'
            }
        }

        stage('Verification') {
            steps {
                sh 'kubectl get deployments'
                sh 'kubectl get pods'
                sh 'kubectl get svc studentapp-service'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}