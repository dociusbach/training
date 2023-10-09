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
                    sh 'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 730074989023.dkr.ecr.us-east-1.amazonaws.com'
                    echo 'Building Docker image'
                    sh "docker build -t 730074989023.dkr.ecr.us-east-1.amazonaws.com/myrepo:1.0 ."
                    
                }
            }
            stage('Stage'){
                steps{
                    echo 'Stage Container in ECR'
                    sh "docker push 730074989023.dkr.ecr.us-east-1.amazonaws.com/myrepo:1.0"
                }
            }
    
        }
}

