pipeline {

```
agent any

parameters {
    choice(
        name: 'SERVICE',
        choices: ['HELM', 'LOGIN'],
        description: 'Select the microservice to build and deploy'
    )
}

environment {
    CLUSTER_NAME = "helm"
    PATH = "/usr/local/bin:/opt/homebrew/bin:${env.PATH}"
}

stages {

    stage('Check Tools') {
        steps {
            sh '''
                echo "========================================"
                echo "Checking Required Tools"
                echo "========================================"

                docker --version
                kind version
                kubectl version --client
                helm version
            '''
        }
    }

    stage('Debug Jenkins Environment') {
        steps {
            sh '''
                echo "========================================"
                echo "Current User"
                echo "========================================"
                whoami

                echo "========================================"
                echo "Current Directory"
                echo "========================================"
                pwd

                echo "========================================"
                echo "PATH"
                echo "========================================"
                echo $PATH

                echo "========================================"
                echo "Docker Location"
                echo "========================================"
                which docker

                echo "========================================"
                echo "Docker Version"
                echo "========================================"
                docker version

                echo "========================================"
                echo "Kind Location"
                echo "========================================"
                which kind

                echo "========================================"
                echo "Kind Version"
                echo "========================================"
                kind version

                echo "========================================"
                echo "Docker Context"
                echo "========================================"
                docker context ls
                docker context show

                echo "========================================"
                echo "Docker Information"
                echo "========================================"
                docker info
            '''
        }
    }

    stage('Set Service Configuration') {
        steps {
            script {

                if (params.SERVICE == 'HELM') {

                    env.SERVICE_PATH = "services/application"
                    env.IMAGE_NAME = "helm"
                    env.CHART_PATH = "./helm-charts/helm-learning-chart"
                    env.RELEASE_NAME = "helm-learning"
                    env.DEPLOYMENT_NAME = "helm-learning-helm-learning-app"

                } else if (params.SERVICE == 'LOGIN') {

                    env.SERVICE_PATH = "services/login"
                    env.IMAGE_NAME = "login"
                    env.CHART_PATH = "./helm-charts/login"
                    env.RELEASE_NAME = "login-release"
                    env.DEPLOYMENT_NAME = "login-release-login-app"

                } else {

                    error("Invalid service selected: ${params.SERVICE}")
                }

                echo "========================================"
                echo "Selected Service: ${params.SERVICE}"
                echo "Service Path: ${env.SERVICE_PATH}"
                echo "Image Name: ${env.IMAGE_NAME}"
                echo "Chart Path: ${env.CHART_PATH}"
                echo "Release Name: ${env.RELEASE_NAME}"
                echo "Deployment Name: ${env.DEPLOYMENT_NAME}"
                echo "========================================"
            }
        }
    }

    stage('Verify Service Files') {
        steps {
            sh '''
                echo "========================================"
                echo "Verifying Service Files"
                echo "========================================"

                echo "Service Path: ${SERVICE_PATH}"

                ls -la ${SERVICE_PATH}

                echo "Checking Dockerfile..."
                test -f ${SERVICE_PATH}/Dockerfile

                echo "Checking app.py..."
                test -f ${SERVICE_PATH}/app.py

                echo "Checking requirements.txt..."
                test -f ${SERVICE_PATH}/requirements.txt

                echo "All required files are present."
            '''
        }
    }

    stage('Build Docker Image') {
        steps {
            sh '''
                echo "========================================"
                echo "Building Docker Image"
                echo "========================================"

                echo "Image: ${IMAGE_NAME}:${BUILD_NUMBER}"
                echo "Build Context: ${SERVICE_PATH}"

                docker build \
                    -t ${IMAGE_NAME}:${BUILD_NUMBER} \
                    ${SERVICE_PATH}

                echo "========================================"
                echo "Verifying Docker Image"
                echo "========================================"

                docker images | grep ${IMAGE_NAME}
            '''
        }
    }

    stage('Load Image into Kind') {
        steps {
            sh '''
                set -x

                echo "========================================"
                echo "Loading Image into Kind Cluster"
                echo "========================================"

                echo "Cluster: ${CLUSTER_NAME}"
                echo "Image: ${IMAGE_NAME}:${BUILD_NUMBER}"

                /opt/homebrew/bin/kind load docker-image \
                    ${IMAGE_NAME}:${BUILD_NUMBER} \
                    --name ${CLUSTER_NAME}

                echo "========================================"
                echo "Verifying Image Inside Kind Nodes"
                echo "========================================"

                echo "Control Plane:"
                docker exec ${CLUSTER_NAME}-control-plane \
                    crictl images | grep ${IMAGE_NAME} || true

                echo "Worker 1:"
                docker exec ${CLUSTER_NAME}-worker \
                    crictl images | grep ${IMAGE_NAME} || true

                echo "Worker 2:"
                docker exec ${CLUSTER_NAME}-worker2 \
                    crictl images | grep ${IMAGE_NAME} || true
            '''
        }
    }

    stage('Deploy using Helm') {
        steps {
            sh '''
                echo "========================================"
                echo "Deploying Using Helm"
                echo "========================================"

                echo "Release Name: ${RELEASE_NAME}"
                echo "Chart Path: ${CHART_PATH}"
                echo "Image: ${IMAGE_NAME}:${BUILD_NUMBER}"

                helm upgrade --install \
                    ${RELEASE_NAME} \
                    ${CHART_PATH} \
                    --set image.repository=${IMAGE_NAME} \
                    --set image.tag=${BUILD_NUMBER} \
                    --set image.pullPolicy=IfNotPresent
            '''
        }
    }

    stage('Verify Deployment') {
        steps {
            sh '''
                echo "========================================"
                echo "Waiting for Deployment Rollout"
                echo "========================================"

                kubectl rollout status \
                    deployment/${DEPLOYMENT_NAME} \
                    --timeout=120s

                echo "========================================"
                echo "Helm Release Status"
                echo "========================================"

                helm status ${RELEASE_NAME}

                echo "========================================"
                echo "Kubernetes Pods"
                echo "========================================"

                kubectl get pods

                echo "========================================"
                echo "Kubernetes Services"
                echo "========================================"

                kubectl get services
            '''
        }
    }
}

post {

    success {
        echo "========================================"
        echo "${params.SERVICE} microservice deployed successfully!"
        echo "========================================"
    }

    failure {
        echo "========================================"
        echo "Pipeline failed. Check the Jenkins console output."
        echo "========================================"
    }
}
```

}
