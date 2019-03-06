#!/usr/bin/env groovy

//Test coverage comparison with master branch https://plugins.jenkins.io/github-pr-coverage-status
//TODO think about SonarCube implementation
@Library('github.com/CornerCaseTechnologies/jenkins-helpers@master') _
node {
	try {
		stage('Build') {
			echo 'Building...'
			postNotifySlack 'STARTED'
			checkout scm
			def scmVars = checkout scm
			def branchName = scmVars.GIT_BRANCH
			echo branchName
		}
		stage('CleaningBefore') {
			echo 'Cleaning before tests'
			sh "bin/deploy_clean.sh"
		}
		stage('TestBackend') {
			echo 'Testing backend'
			sh "bin/deploy_test.sh"
		}
		stage('GenerateTestsCoverageXML') {
			echo 'Generating tests coverage'
			sh "bin/coverage.sh"
			container_name = sh(
					script: "docker ps -a --format '{{.Names}}' | grep django_run_2",
					returnStdout: true
			).trim()
			sh "docker cp ${container_name}:/app/coverage.xml ."
			step([$class: 'CoberturaPublisher', autoUpdateHealth: false, autoUpdateStability: false, coberturaReportFile: '**/coverage.xml', failUnhealthy: false, failUnstable: false, maxNumberOfBuilds: 0, onlyStable: false, sourceEncoding: 'ASCII', zoomCoverageChart: false])
		}
		stage('CleaningAfter') {
			echo 'Cleaning after tests'
			sh "bin/deploy_clean.sh"
		}
	} catch (e) {
		// If there was an exception thrown, the build failed
		currentBuild.result = "FAILED"
		throw e
	} finally {
		// Success or failure, always send notifications
		postNotifySlack currentBuild.result
	}


}
