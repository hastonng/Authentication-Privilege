pipeline {
    agent { 
        node {
            label 'docker-agent-python'
            }
      }
      triggers {
        pollSCM '*/1 * * * *'
    }
    stages {
        stage('Build') {
            steps {
                echo "Building.."
                sh '''
                pip install pandas
                pip install numpy
                pip install openpyxl
                pip install pyinstaller
                '''
            }
        }
        stage('Test') {
            steps {
                echo "Testing.."
                sh '''
                echo "doing test stuff.."
                '''
            }
        }
        stage('Deliver') {
            steps {
                echo 'Deliver....'
                sh '''
                echo "doing delivery stuff.."
                '''
            }
        }
    }
}