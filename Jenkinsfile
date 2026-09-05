pipeline {


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
                echo "Checking required tools..."
                docker --version
                kind version
                kubectl version --client
                helm version
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
                }

                echo "Selected Service: ${params.SERVICE}"
                echo "Service Path: ${env.SERVICE_PATH}"
                echo "Image Name: ${env.IMAGE_NAME}"
                echo "Chart Path: ${env.CHART_PATH}"
                echo "Release Name: ${env.RELEASE_NAME}"
                echo "Deployment Name: ${env.DEPLOYMENT_NAME}"
            }
        }
    }

    stage('Build Docker Image') {
        steps {
            sh '''
                echo "Building Docker image..."

                docker build \
                -t ${IMAGE_NAME}:${BUILD_NUMBER} \
                ${SERVICE_PATH}
            '''
        }
    }

    stage('Load Image into Kind') {
        steps {
            sh '''
                echo "Loading image into Kind cluster..."

                kind load docker-image \
                ${IMAGE_NAME}:${BUILD_NUMBER} \
                --name ${CLUSTER_NAME}
            '''
        }
    }

    stage('Deploy using Helm') {
        steps {
            sh '''
                echo "Deploying ${SERVICE} using Helm..."

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
                echo "Waiting for deployment rollout..."

                kubectl rollout status \
                deployment/${DEPLOYMENT_NAME} \
                --timeout=120s

                echo "Checking Helm release..."
                helm status ${RELEASE_NAME}

                echo "Checking Kubernetes resources..."
                kubectl get pods
                kubectl get services
            '''
        }
    }
}

post {
    success {
        echo "${params.SERVICE} microservice deployed successfully!"
    }

    failure {
        echo "Pipeline failed. Check the Jenkins console output."
    }
}


}
