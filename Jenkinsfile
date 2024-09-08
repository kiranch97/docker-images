pipeline {
    agent any
    environment {
        DOCKER_IMAGE_NAME = "rahul4884/train-schedule"
    }
    stages {
        stage("Checkout from github repo"){
            steps{
            git url: 'https://github.com/Patelrahul4884/cicd-pipeline-train-schedule-autodeploy.git'
            }
        }
        stage('Build') {
            steps {
                echo 'Running build automation'
                sh './gradlew build --no-daemon --scan'
                archiveArtifacts artifacts: 'dist/trainSchedule.zip'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    app = docker.build(DOCKER_IMAGE_NAME)
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'docker_hub_login') {
                        app.push("${env.BUILD_NUMBER}")
                        app.push("latest")
                    }
                }
            }
        }
        stage('DeployToProduction') {
            steps {
                kubeconfig(caCertificate: 'LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURJVENDQWdtZ0F3SUJBZ0lJZFByay95K0ZnWUF3RFFZSktvWklodmNOQVFFTEJRQXdGVEVUTUJFR0ExVUUKQXhNS2EzVmlaWEp1WlhSbGN6QWVGdzB5TkRBeE1qRXhNak14TkROYUZ3MHlOVEF4TWpBeE1qTTJORFZhTURReApGekFWQmdOVkJBb1REbk41YzNSbGJUcHRZWE4wWlhKek1Sa3dGd1lEVlFRREV4QnJkV0psY201bGRHVnpMV0ZrCmJXbHVNSUlCSWpBTkJna3Foa2lHOXcwQkFRRUZBQU9DQVE4QU1JSUJDZ0tDQVFFQW5kMktNRGl0NFpidE1pdjMKU3pwdEVUNUhaVm5memtnOUpQeXEzeDNBRHpCY2NZWWxIYUpjZVNVNHZCRFJDVUdHeDAwaFBDRlIzT2tIRjJWYwpNaDZ3MWRhUkJrU3BseFQ5UGoxa3RLWFNEM3hyU3NBU3FwODdaZ3VoR1BVTDl1MUVibTJUTHMwTlpVOUVuOWtECllSWmhZQzV6bm5veEtlMjdUNWwwWUlUbkJ2TDM0UzB2T0dxVk5NMUZOdHdpcW91eXM3cVZvd1NPWUxMVU1tYVoKbnVrd0pzQXljY0MvTDVTOWd3MVViM1prZUNjYnMxVzYvREhQYUFmMUt6VzNPNDVOS1I1TlQ2dHFNR0pucGtaSwpWVzJJL2Vud1pUeXpWYkErUFo0ZFRGWnIzQlNXUkdzK3JJOC8vbTNFeEZXTWtXOUtjK1lqU2VwejB0Nk9tZDllCjVUZVFsd0lEQVFBQm8xWXdWREFPQmdOVkhROEJBZjhFQkFNQ0JhQXdFd1lEVlIwbEJBd3dDZ1lJS3dZQkJRVUgKQXdJd0RBWURWUjBUQVFIL0JBSXdBREFmQmdOVkhTTUVHREFXZ0JUZGlROTFvYm4xaW4vQXk0bGdRMlQzL0VvZAp1ekFOQmdrcWhraUc5dzBCQVFzRkFBT0NBUUVBQ2RxZVNTbi91djNuQlBjZldPbGFnU0RiRnRaWlpkV3htajVyCm8wcUxydkw3MTNNUXNINHVKNTlXQXI0RGZUNjBNRVo2cXFTZHJyZHg4aWZmWlN3d3hIQUp4ZVMrMzNuWGFHZU4Kd3ZtSmgyOHhGK3FrM1p2dldVM2IyRUhjaUxCOHZSYk8rNHkrUm1ZVVA4dENVZ2J4dlZpcC9MbTJ2d1MxWW9hSwpIc2NoQ2tNMDRGMTdLc2hsNC9hRThjMVB0dUNDNFRCSnUvQUJqTC9kZnN2SDN6em9oZ29wYWVGWkY2b3VrTXhCClRuemNLSmVRRkVJa0MweWdZcUhleXdNWis1U213c0N5MUhUWldKN2xPRlJtSkV2d0Z3dlRDYlpRMjB1eUxHWk0KRzlsaG1JWFpkZ0VSN25nK1Z5Z0NSK0pVTzBtQjk2a0d0dlNDSVJnaHVPOVhMWW03RGc9PQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCg==', credentialsId: 'kubernetes', serverUrl: 'https://10.8.79.195:6443') {
    // some block
                 sh 'kubectl apply -f deployment.yaml'
                 sh 'kubectl apply -f app-service.yaml'
                 sh 'kubectl rollout restart deployment train-schedule'
}
            }
        }
    }
}
