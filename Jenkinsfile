pipeline {
    agent any

    environment {
        DOCKER_CREDS = credentials('dockerhub-creds')
        BEST_ACCURACY = credentials('best-accuracy')
        IMAGE_NAME = "yourdockerhubusername/ml-model"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Virtual Environment') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Train Model') {
            steps {
                sh '''
                . venv/bin/activate
                python train.py
                '''
            }
        }

        stage('Read Accuracy') {
            steps {
                script {
                    def metrics = readJSON file: 'app/artifacts/metrics.json'
                    env.CURRENT_ACCURACY = metrics.accuracy.toString()
                    echo "Current Accuracy: ${env.CURRENT_ACCURACY}"
                }
            }
        }

        stage('Compare Accuracy') {
            steps {
                script {
                    if (env.CURRENT_ACCURACY.toFloat() > BEST_ACCURACY.toFloat()) {
                        env.BUILD_IMAGE = "true"
                        echo "New model is better!"
                    } else {
                        env.BUILD_IMAGE = "false"
                        echo "New model is NOT better."
                    }
                }
            }
        }

        stage('Build Docker Image') {
            when {
                expression { env.BUILD_IMAGE == "true" }
            }
            steps {
                sh """
                docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .
                docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest
                """
            }
        }

        stage('Push Docker Image') {
            when {
                expression { env.BUILD_IMAGE == "true" }
            }
            steps {
                sh """
                echo ${DOCKER_CREDS_PSW} | docker login -u ${DOCKER_CREDS_USR} --password-stdin
                docker push ${IMAGE_NAME}:${BUILD_NUMBER}
                docker push ${IMAGE_NAME}:latest
                """
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'app/artifacts/**', fingerprint: true
        }
    }
}
