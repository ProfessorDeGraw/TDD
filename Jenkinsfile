pipeline {
    agent any
    stages {
        stage('Functional Tests') {
            steps {
                withPythonEnv('tdd35') {
                    pysh ( script: 'pip install tox' )
                        pysh ( script: 'tox' )
                }
            }
        }
    }
}