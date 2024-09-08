pipeline {
    agent any

    environment {
        REGISTRY = "your-dockerhub-username"
        IMAGE_NAME = "sample-app"
        KUBE_NAMESPACE = "default"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'master', url: '<your-git-repo-url>'
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
