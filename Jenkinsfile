pipeline {

agent any

parameters {
    choice(
        name: 'SERVICE',
        choices: ['HELM', 'LOGIN', 'PAYMENTS'],
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

    stage('Configure Service') {
        steps {
            script {

                if (params.SERVICE == 'HELM') {
                    env.IMAGE_NAME = 'helm'
                    env.SERVICE_PATH = 'services/application'
                    env.CHART_PATH = './helm-charts/helm-learning-chart'
                    env.RELEASE_NAME = 'helm'
                    env.DEPLOYMENT_NAME = 'helm'
                }

                else if (params.SERVICE == 'LOGIN') {
                    env.IMAGE_NAME = 'login'
                    env.SERVICE_PATH = 'services/login'
                    env.CHART_PATH = './helm-charts/login'
                    env.RELEASE_NAME = 'login'
                    env.DEPLOYMENT_NAME = 'login'
                }

               else if (params.SERVICE == 'PAYMENTS') {
                    env.IMAGE_NAME = 'payments'
                    env.SERVICE_PATH = 'services/payments'
                    env.CHART_PATH = './helm-charts/payments'
                    env.RELEASE_NAME = 'payments-release'
                    env.DEPLOYMENT_NAME = 'payments'
                }

                echo "Selected service: ${params.SERVICE}"
                echo "Image: ${env.IMAGE_NAME}"
                echo "Service path: ${env.SERVICE_PATH}"
                echo "Chart path: ${env.CHART_PATH}"
                echo "Release name: ${env.RELEASE_NAME}"
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

    // stage('Load Image into Kind') {
    //     steps {
    //         sh '''
    //             echo "Loading image into Kind cluster..."

    //             kind load docker-image \
    //             ${IMAGE_NAME}:${BUILD_NUMBER} \
    //             --name ${CLUSTER_NAME}
    //         '''
    //     }
    // }
    stage('Load Image into Kind') {
    steps {
        script {
            retry(3) {
                sh '''
                    echo "Loading image into Kind cluster..."

                    kind load docker-image \
                        ${IMAGE_NAME}:${BUILD_NUMBER} \
                        --name ${CLUSTER_NAME}
                '''
            }
        }
    }
}

    stage('Deploy using Helm') {
        steps {
            sh '''
                echo "Deploying ${IMAGE_NAME} using Helm..."

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

                echo ""
                echo "Pods:"
                kubectl get pods

                echo ""
                echo "Services:"
                kubectl get services

                echo ""
                echo "Helm Release:"
                helm status ${RELEASE_NAME}
            '''
        }
    }
}

post {

    success {
        echo "${params.SERVICE} microservice deployed successfully!"
    }

    failure {
        echo "Pipeline failed. Check the console output."
    }
}


}
