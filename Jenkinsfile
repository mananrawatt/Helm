pipeline {

    agent any

    parameters {
        choice(
            name: 'SERVICE',
            choices: [
                'HELM',
                'LOGIN',
                'PAYMENTS',
                'COMMON',
                'TAGS',
                'GATEWAY'
            ],
            description: 'Select the microservice to build and deploy'
        )
    }

    environment {
        CLUSTER_NAME = 'helm'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Configure Service') {
            steps {
                script {

                    if (params.SERVICE == 'HELM') {

                        env.IMAGE_NAME = 'helm'
                        env.SERVICE_PATH = 'services/application'
                        env.CHART_PATH = './helm-charts/helm-learning-chart'
                        env.VALUES_FILE = ''
                        env.RELEASE_NAME = 'helm'
                        env.DEPLOYMENT_NAME = 'helm'

                    } else if (params.SERVICE == 'LOGIN') {

                        env.IMAGE_NAME = 'login'
                        env.SERVICE_PATH = 'services/login'
                        env.CHART_PATH = './helm-charts/login'
                        env.VALUES_FILE = ''
                        env.RELEASE_NAME = 'login'
                        env.DEPLOYMENT_NAME = 'login'

                    } else if (params.SERVICE == 'PAYMENTS') {

                        env.IMAGE_NAME = 'payments'
                        env.SERVICE_PATH = 'services/payments'
                        env.CHART_PATH = './helm-charts/payments'
                        env.VALUES_FILE = ''
                        env.RELEASE_NAME = 'payments'
                        env.DEPLOYMENT_NAME = 'payments'

                    } else if (params.SERVICE == 'COMMON') {

                        env.IMAGE_NAME = 'common'
                        env.SERVICE_PATH = 'services/common'
                        env.CHART_PATH = './helm-charts/generic-microservice'
                        env.VALUES_FILE = './helm-charts/generic-microservice/microservices/common.yaml'
                        env.RELEASE_NAME = 'common'
                        env.DEPLOYMENT_NAME = 'common'

                    } else if (params.SERVICE == 'TAGS') {

                        env.IMAGE_NAME = 'tags'
                        env.SERVICE_PATH = 'services/tags'
                        env.CHART_PATH = './helm-charts/generic-microservice'
                        env.VALUES_FILE = './helm-charts/generic-microservice/microservices/tags.yaml'
                        env.RELEASE_NAME = 'tags'
                        env.DEPLOYMENT_NAME = 'tags'

                    } else if (params.SERVICE == 'GATEWAY') {

                        env.IMAGE_NAME = 'gateway'
                        env.SERVICE_PATH = 'services/gateway'
                        env.CHART_PATH = './helm-charts/generic-microservice'
                        env.VALUES_FILE = './helm-charts/generic-microservice/microservices/gateway.yaml'
                        env.RELEASE_NAME = 'gateway'
                        env.DEPLOYMENT_NAME = 'gateway'
                    }

                    env.IMAGE_TAG = "v${env.BUILD_NUMBER}"

                    echo """
                    ========================================
                    SERVICE       : ${params.SERVICE}
                    IMAGE         : ${env.IMAGE_NAME}:${env.IMAGE_TAG}
                    SERVICE PATH  : ${env.SERVICE_PATH}
                    CHART PATH    : ${env.CHART_PATH}
                    VALUES FILE   : ${env.VALUES_FILE}
                    RELEASE       : ${env.RELEASE_NAME}
                    DEPLOYMENT    : ${env.DEPLOYMENT_NAME}
                    ========================================
                    """
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                    echo "Building Docker image..."
                    docker build \
                        -t ${IMAGE_NAME}:${IMAGE_TAG} \
                        ${SERVICE_PATH}
                """
            }
        }

        stage('Load Image into Kind') {
            steps {
                sh """
                    echo "Loading ${IMAGE_NAME}:${IMAGE_TAG} into Kind..."
                    kind load docker-image \
                        ${IMAGE_NAME}:${IMAGE_TAG} \
                        --name ${CLUSTER_NAME}
                """
            }
        }

        stage('Deploy with Helm') {
            steps {
                sh """
                    echo "Deploying ${IMAGE_NAME}:${IMAGE_TAG}..."

                    helm upgrade --install ${RELEASE_NAME} ${CHART_PATH} \
                        ${VALUES_FILE ? "-f ${VALUES_FILE}" : ""} \
                        --set image.repository=${IMAGE_NAME} \
                        --set image.tag=${IMAGE_TAG} \
                        --set image.pullPolicy=IfNotPresent
                """
            }
        }

        stage('Verify Deployment') {
            steps {
                sh """
                    echo "Waiting for deployment rollout..."

                    kubectl rollout status \
                        deployment/${DEPLOYMENT_NAME} \
                        --timeout=120s

                    echo ""
                    echo "========================================"
                    echo "PODS"
                    echo "========================================"

                    kubectl get pods -o wide

                    echo ""
                    echo "========================================"
                    echo "SERVICES"
                    echo "========================================"

                    kubectl get services

                    echo ""
                    echo "========================================"
                    echo "HELM RELEASE"
                    echo "========================================"

                    helm status ${RELEASE_NAME}
                """
            }
        }
    }

    post {
        success {
            echo """
            ========================================
            DEPLOYMENT SUCCESSFUL
            ========================================

            Service : ${params.SERVICE}
            Image   : ${IMAGE_NAME}:${IMAGE_TAG}
            Release : ${RELEASE_NAME}
            """
        }

        failure {
            echo """
            ========================================
            DEPLOYMENT FAILED
            ========================================

            Service : ${params.SERVICE}
            Image   : ${IMAGE_NAME}:${IMAGE_TAG}
            """
        }
    }
}