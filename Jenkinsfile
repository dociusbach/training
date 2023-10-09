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
                    echo 'build docker'
                }
            }
            stage('Stage'){
                steps{
                    echo 'Stage Container'
                }
            }
    
        }
}

