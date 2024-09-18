pipeline {
    agent any
    tools {
        nodejs 'node16'  
    }
    environment {
        SCANNER_HOME = tool 'sonar-scanner'
    }
    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }
        stage('Checkout from Git') {
            steps {
                git branch: 'main', url: 'https://github.com/The-Cloud-Guy/pyquotes.git'  
            }
        }
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonar-server') {
                    sh '''
                        $SCANNER_HOME/bin/sonar-scanner \
                        -Dsonar.projectName=pyquotes-app \
                        -Dsonar.projectKey=pyquotes-app
                    '''
                }
            }
        }
        stage('Quality Gate') {
            steps {
                script {
                    waitForQualityGate abortPipeline: false, credentialsId: 'Sonar-token'
                }
            }
        }
        stage('Install Dependencies') {
            steps {
                sh "pip install -r requirements.txt"
            }
        }
        stage('OWASP Dependency Check') {
            steps {
                dependencyCheck additionalArguments: '--scan ./ --format XML', odcInstallation: 'DP-Check'
                dependencyCheckPublisher pattern: '**/dependency-check-report.xml'
            }
        }
        stage('File System Scan') {
            steps {
                sh "trivy fs --format table -o trivy-fs-report.html ."
            }
        }
        stage('Build & Tag Docker Image') {
            steps {
               script {
                   withDockerRegistry(credentialsId: 'docker-cred', toolName: 'docker') {
                            sh "docker build -t redditclone thecloudguyn/programmingquotes:latest ."
                    }
               }
            }
        }        
        stage('Docker Image Scan') {
            steps {
                sh "trivy image --format table -o trivy-image-report.html redditclone hecloudguyn/programmingquotes:latest "
            }
        }       
        stage('Push Docker Image') {
            steps {
               script {
                   withDockerRegistry(credentialsId: 'docker-cred', toolName: 'docker') {
                            sh "docker push redditclone thecloudguyn/programmingquotes:latest"
                    }
               }
            }
        }
        stage('Update Helm Chart Version') {
            steps {
                script {
                    def helmChartPath = 'helm-Chart/Chart.yaml'
                    
                    sh '''
                        NEW_VERSION=$(date +'%Y.%m.%d-%H.%M')
                        sed -i "s/^version:.*/version: ${NEW_VERSION}/" helm-Chart/Chart.yaml
                        echo "Updated Helm chart version to ${NEW_VERSION}"
                    '''
                }
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    withKubeConfig(credentialsId: 'k8s') {
 
                        sh '''
                            helm upgrade --install nodejs-app ./helm-files \
                            --set image.repository=thecloudguyn/programmingquotes\
                            --set image.tag=latest
                        '''
                    }
                }
            }
        }
    }
    post {
        always {
            script {
                def recipientList = "recipient@gmail.com"  
                def subject = "${currentBuild.currentResult}: Job ${env.JOB_NAME} Build ${env.BUILD_NUMBER}"
                def body = """<p>Job Name: ${env.JOB_NAME}</p>
                              <p>Build Number: ${env.BUILD_NUMBER}</p>
                              <p>Build Status: ${currentBuild.currentResult}</p>
                              <p>More details at: <a href='${env.BUILD_URL}'>${env.BUILD_URL}</a></p>"""

                emailext (
                    to: recipientList,
                    subject: subject,
                    body: body,
                    mimeType: 'text/html'
                    attachmentsPattern: 'trivy-fs-report.html,trivy-image-report.html' 
                )
            }
        }
    }
}
