pipeline {
    agent any
    stages {
        stage('Clone git') {
            steps {
                git branch: 'main', url: 'https://github.com/pawelgoj/load_testing_with_locust.git'
            }
        }
        stage('Build') {
            steps {
                bat 'C:\\Users\\pagoj\\AppData\\Local\\Programs\\Python\\Python311\\python -m pip install -r requirements.txt'
                bat '@ECHO off\n' +
                    '( ECHO USER=%NAME% & ECHO PASSWORD=%PASSWORD% & ECHO PATHTOMYSQLDUMP=%PATHTOMYSQLDUMP% & ECHO PATHTOMYSQL=%PATHTOMYSQL% ) > .env\n'
                bat 'mkdir data_base_backup'
            }
        }
        stage('Test') {
            steps {
                bat 'C:\\Users\\pagoj\\AppData\\Local\\Programs\\Python\\Python311\\Scripts\\locust -f .\\locustfiles\\locustfile.py,.\\shapes\\three_waves.py --config=locust.conf  --html report.html'
            }
        }
        stage('Report') {
            steps {
                publishHTML([allowMissing: true, alwaysLinkToLastBuild: false, keepAll: false, reportDir: '', reportFiles: 'report.html', reportName: 'HTML Report', reportTitles: '', useWrapperFileDirectly: true])
            }
        }
    }
}