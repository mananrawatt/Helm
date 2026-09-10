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

        // macOS tool paths
        DOCKER = '/usr/local/bin/docker'
        KIND = '/opt/homebrew/bin/kind'
        KUBECTL = '/opt/homebrew/bin/kubectl'
        HELM = '/opt/homebrew/bin/helm'

        PATH = "/usr/local/bin:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/bin:/bin:/usr/sbin:/sbin"
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

                    // Image tag = v + Jenkins build number
                    env.IMAGE_TAG = "v${env.BUILD_NUMBER}"

                    echo """
==================================================
SERVICE        : ${params.SERVICE}
IMAGE          : ${env.IMAGE_NAME}:${env.IMAGE_TAG}
SERVICE PATH   : ${env.SERVICE_PATH}
CHART PATH     : ${env.CHART_PATH}
VALUES FILE    : ${env.VALUES_FILE}
RELEASE NAME   : ${env.RELEASE_NAME}
DEPLOYMENT     : ${env.DEPLOYMENT_NAME}
CLUSTER        : ${env.CLUSTER_NAME}
==================================================
"""
                }
            }
        }

        stage('Check Tools') {
            steps {
                sh """
                    echo "Checking required tools..."

                    ${DOCKER} --version
                    ${KIND} version
                    ${KUBECTL} version --client
                    ${HELM} version
                """
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                    echo "Building Docker image..."
                    ${DOCKER} build \
                        -t ${IMAGE_NAME}:${IMAGE_TAG} \
                        ${SERVICE_PATH}
                """
            }
        }

        stage('Load Image into Kind') {
            steps {
                sh """
                    echo "Loading ${IMAGE_NAME}:${IMAGE_TAG} into Kind..."

                    ${KIND} load docker-image \
                        ${IMAGE_NAME}:${IMAGE_TAG} \
                        --name ${CLUSTER_NAME}
                """
            }
        }

        stage('Deploy with Helm') {
            steps {
                script {

                    if (env.VALUES_FILE?.trim()) {

                        sh """
                            echo "Deploying using generic Helm chart..."

                            ${HELM} upgrade --install \
                                ${RELEASE_NAME} \
                                ${CHART_PATH} \
                                -f ${VALUES_FILE} \
                                --set image.repository=${IMAGE_NAME} \
                                --set image.tag=${IMAGE_TAG} \
                                --set image.pullPolicy=IfNotPresent
                        """

                    } else {

                        sh """
                            echo "Deploying using service-specific Helm chart..."

                            ${HELM} upgrade --install \
                                ${RELEASE_NAME} \
                                ${CHART_PATH} \
                                --set image.repository=${IMAGE_NAME} \
                                --set image.tag=${IMAGE_TAG} \
                                --set image.pullPolicy=IfNotPresent
                        """
                    }
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                sh """
                    echo "Waiting for deployment rollout..."

                    ${KUBECTL} rollout status \
                        deployment/${DEPLOYMENT_NAME} \
                        --timeout=120s

                    echo ""
                    echo "=================================================="
                    echo "DEPLOYMENTS"
                    echo "=================================================="

                    ${KUBECTL} get deployments

                    echo ""
                    echo "=================================================="
                    echo "PODS"
                    echo "=================================================="

                    ${KUBECTL} get pods -o wide

                    echo ""
                    echo "=================================================="
                    echo "SERVICES"
                    echo "=================================================="

                    ${KUBECTL} get services

                    echo ""
                    echo "=================================================="
                    echo "HELM RELEASE"
                    echo "=================================================="

                    ${HELM} status ${RELEASE_NAME}
                """
            }
        }
    }

    post {

        success {
            echo """
==================================================
DEPLOYMENT SUCCESSFUL
==================================================

Service       : ${params.SERVICE}
Image         : ${env.IMAGE_NAME}:${env.IMAGE_TAG}
Release       : ${env.RELEASE_NAME}
Deployment    : ${env.DEPLOYMENT_NAME}
Cluster       : ${env.CLUSTER_NAME}

==================================================
"""
        }

        failure {
            echo """
==================================================
DEPLOYMENT FAILED
==================================================

Service       : ${params.SERVICE}
Image         : ${env.IMAGE_NAME}:${env.IMAGE_TAG}

Please check the Jenkins console output.

==================================================
"""
        }
    }
}