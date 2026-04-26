pipeline {
    agent any

    environment {
        IMAGE_NAME = "neeraj6672/rollback-app"
    }

    stages {

        stage('Build Image') {
            steps {
                echo "🔨 Building Docker image v2..."
                sh "docker build -t ${IMAGE_NAME}:v2 ."
            }
        }

        stage('Push to DockerHub') {
            steps {
                echo "📦 Pushing to DockerHub..."
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'USER',
                    passwordVariable: 'PASS'
                )]) {
                    sh "echo $PASS | docker login -u $USER --password-stdin"
                    sh "docker push ${IMAGE_NAME}:v2"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo "☸️ Deploying v2..."
                sh "kubectl set image deployment/rollback-app rollback-app=${IMAGE_NAME}:v2"
            }
        }

        stage('Test Deployment') {
            steps {
                echo "🧪 Testing app..."
                script {
                    sleep(20)

                    def ip = sh(
                        script: "minikube ip",
                        returnStdout: true
                    ).trim()

                    def response = sh(
                        script: "curl -s -o /dev/null -w '%{http_code}' http://${ip}:30080",
                        returnStdout: true
                    ).trim()

                    echo "HTTP Status: ${response}"

                    if (response != '200') {
                        error("❌ App failed with ${response}")
                    } else {
                        echo "✅ App is healthy"
                    }
                }
            }
        }
    }

    post {
        failure {
            echo "🔁 Rolling back..."
            sh "kubectl rollout undo deployment rollback-app"
        }
        success {
            echo "🎉 Deployment successful!"
        }
    }
}