pipeline {
    agent { 
        node {
            label 'docker-agent-python2'
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
                '''
            }
        }
        stage('Test') {
            steps {
                echo "Testing.."
                sh '''
                echo "doing test stuff.."
                cd Huawei_Authentication_Privellege_WEUDOC

                

                python3 Run.py
                '''
            }
        }
        stage('Deliver') {
            steps {
                echo 'Deliver....'
                sh '''
                echo "doing delivery stuff.."

                echo "Building Run.exe with Pyinstaller..."

                echo "Copying to directory..." 
                '''
            }
        }
    }
}