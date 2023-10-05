pipeline{

    agent any
    stages{
            stage('Test'){
                
                steps{
                    sh 'mvn -f mvn/PortfilioWeb/pom.xml clean package'
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
                    sh 'docker build . -t joshPortfolio:'
                }
            }
            stage('Deploy'){
                steps{
                    echo 'This is the first stage where we are Deploying'
                }
            }
    
        }
}

