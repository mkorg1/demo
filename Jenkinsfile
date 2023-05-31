pipeline {
    agent none
    stages {
        stage("build & SonarQube analysis") {
            agent any
            environment {
                SCANNER_HOME = tool 'SQ_Scanner_Latest'
            }
            steps {
                withSonarQubeEnv('dmeppiel_sq') {
                    sh "$SCANNER_HOME/bin/sonar-scanner"
                }
            }
        }
        stage("Quality Gate") {
            steps {
                timeout(time: 1, unit: 'HOURS') {
                    waitForQualityGate abortPipeline: false
                }
            }
        }
    }
}