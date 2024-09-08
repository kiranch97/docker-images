pipeline {
    agent any

    environment {
        REGISTRY = "kiranch97"
        IMAGE_NAME = "sample-app"
        KUBE_NAMESPACE = "default"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/kiranch97/docker-images'
            }
        }

        stage('Build Image') {
            steps {
                script {
                    dockerImage = docker.build("${REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}")
                }
            }
        }

        stage('Push Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub', passwordVariable: 'DOCKERHUB_PASS', usernameVariable: 'DOCKERHUB_USER')]) {
                    script {
                        docker.withRegistry('', "${DOCKERHUB_USER}:${DOCKERHUB_PASS}") {
                            dockerImage.push()
                        }
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([kubeconfigContent(credentialsId: 'kubeconfig', variable: 'KUBECONFIG_CONTENT')]) {
                    writeFile file: 'kubeconfig', text: "${KUBECONFIG_CONTENT}"
                    sh '''
                    kubectl --kubeconfig=kubeconfig set image deployment/${IMAGE_NAME}-deployment ${IMAGE_NAME}=${REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER} -n ${KUBE_NAMESPACE}
                    '''
                }
            }
        }
    }
}
