pipeline{
    agent any{
        environment{
            Dockerhub_Credential = credential('sanju1701')
            Dockerhub_Image = 'sanju1701/ai-crime-predictor'
        }
        
    stages{
        stage("Checkout"){
            steps{
                git branch : 'main', 
                url : ''
            }
        }
        stage('Docker login'){
            steps{
                sh 'echo $Dockerhub_Credential_Password | docker login -u $Dockerhub_Credential_Username --password-stdin'

            }
        }
        stage('Build docker image'){
            steps{
                sh ''docker build -t $Dockerhub_Image:latest . 
                docker tag $Dockerhub_Image:latest $Dockerhub_Image:$BUILD_NUMBER''
            }
        }
        stage('Deploy'){
            steps{
                sh 'docker push $Dockerhub_Image:latest'
                sh 'docker push $Dockerhub_Image:$BUILD_NUMBER'
                sh 'docker run -d -p 80:80 $Dockerhub_Image:latest'
            }
        }
    
        post{
            success{
                echo 'pipline executed successfully'
            }
            failure{
                echo 'pipeline failed'
            }
               
        }
            
        }   
    }   
}