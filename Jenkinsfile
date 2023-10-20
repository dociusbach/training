pipeline{

    agent any
    stages{
            stage('Test'){
                
                steps{
                    sh 'mvn -f hohtrainingapp/pom.xml clean package'
                }
                post{
                    success{
                        echo "Archiving Package..."
                        archiveArtifacts artifacts: '**/*.war'
                    }
                }
            }
            stage('Create Tomcat Docker'){
                steps{
                    // sh 'docker build . -t joshPortfolio:'

                    echo 'Logging into ECR'

                    sh "docker build -t 079904783278.dkr.ecr.us-east-1.amazonaws.com/23-3-bah-cohort:latest . --no-cache"
                    
                }
            }
            stage('Stage'){
                steps{
                    echo 'Stage Container in ECR'
                    sh script('/bin/bash -c aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 079904783278.dkr.ecr.us-east-1.amazonaws.com/23-3-bah-cohort')
                    echo 'Building Docker image'
                    sh "docker push 079904783278.dkr.ecr.us-east-1.amazonaws.com/23-3-bah-cohort:latest"
                }
            }
    
        }
}

