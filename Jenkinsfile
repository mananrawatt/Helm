pipeline {
    agent any

    environment {
        IMAGE_NAME = "helm"
        CLUSTER_NAME = "helm"
        CHART_PATH = "./helm-learning-chart"
        RELEASE_NAME = "helm-learning"

        PATH = "/usr/local/bin:/opt/homebrew/bin:${env.PATH}"
    }

    stages {

        stage('Check Tools') {
            steps {
                sh '''
                    echo "Checking required tools..."

                    docker --version
                    kind version
                    kubectl version --client
                    helm version
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    echo "Building Docker image..."

                    docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .
                '''
            }
        }

        stage('Load Image into Kind') {
            steps {
                sh '''
                    echo "Loading image into Kind cluster..."

                    kind load docker-image ${IMAGE_NAME}:${BUILD_NUMBER} \
                    --name ${CLUSTER_NAME}
                '''
            }
        }

        stage('Deploy using Helm') {
            steps {
                sh '''
                    echo "Deploying application using Helm..."

                    helm upgrade --install ${RELEASE_NAME} ${CHART_PATH} \
                    --set image.repository=${IMAGE_NAME} \
                    --set image.tag=${BUILD_NUMBER} \
                    --set image.pullPolicy=IfNotPresent
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    echo "Checking Helm release..."
                    helm status ${RELEASE_NAME}

                    echo "Checking Kubernetes resources..."
                    kubectl get pods
                    kubectl get services

                    echo "Waiting for deployment rollout..."
                    kubectl rollout status deployment/${RELEASE_NAME}-helm-learning-app \
                    --timeout=120s
                '''
            }
        }
    }

    post {
        success {
            echo "Application deployed successfully!"
        }

        failure {
            echo "Pipeline failed. Check the console output."
        }
    }
}
