pipeline {
    agent any  // This tells Jenkins to run the pipeline on any available agent

    tools {
        // Specify the Maven installation to use
        maven 'Maven 3.8.1'  // Make sure this matches a Maven installation name in your Jenkins configuration
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout your code from version control
                checkout scm
            }
        }

        stage('Build') {
            steps {
                // Run Maven build
                sh 'mvn clean package'
            }
        }

        stage('Docker Build and Push') {
            steps {
                // Build and push Docker image
                script {
                    docker.withRegistry('https://hub.docker.com', 'docker-registry-credentials') {
                        def customImage = docker.build("kiranch97/kiran-app:${env.BUILD_NUMBER}")
                        customImage.push()
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                // Add your deployment steps here
                // For example, you might use a shell script to deploy to your environment
                sh 'kubectl apply -f kubernetes-deployment.yaml'
            }
        }
    }

    post {
        always {
            // Clean up workspace
            cleanWs()
        }
    }
}
