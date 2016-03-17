## Getting started ##

Sputnik supports Java, Groovy and Scala projects build with Maven or Gradle.
This tutorial shows how to configure and use Sputnik in a few short steps.

Table of contents
=================
  * [Login to Sputnik with GitHub account](#login-to-sputnik-with-github-account)
  * [Authorize Sputnik to use your GitHub account](#authorize-sputnik-to-use-your-github-account)
  * [Check projects to be analyzed](#check-projects-to-be-analyzed)
  * [Configure your Travis-CI or CircleCI account](#configure-your-travis-ci-or-circleci-account)
  * [Configure Sputnik in your project](#configure-sputnik-in-your-project)
  * [Build Project and read Sputnik comments](#build-project-and-read-sputnik-comments)

#### Login to Sputnik with GitHub account
------------------------------------
Go to http://sputnik.touk.pl to log into Sputnik with GitHub account:
![alt text](https://raw.githubusercontent.com/lordOfSputnik/sputnik-test/master/readme-resources/sputnik_01_login_with_github.png)



Authorize Sputnik to use your GitHub account
--------------------------------------------
Sputnik writes results of code analyses in GitHub, so it needs to have an access to your account.
2_authorize_application.png

Check projects to be analyzed
-----------------------------
Go to http://sputnik.touk.pl/app, press Sync Repos to see list of all your GitHub repositories.
3_sync_repos_check_projects.png

Now check all projects that you'd like to work with Sputnik
3_sync_repos_check_projects_marked.png

For a selected project you can customize set of rules that will be applied in the code analysis:
3_project_settings_v1.png

Configure your Travis-CI account
--------------------------------
Once you have configured Travis-CI account make sure the projects that have been marked in Sputnik are also selected in Travis-CI:
4_travis_conf.png

Configure Sputnik in your project
---------------------------------
Edit .travis.yml with shell command that starts sputnik analyses
{code - boldem after_success i następna linijka}
language: java
jdk:
- oraclejdk8
after_success:
- bash <(curl -s https://raw.githubusercontent.com/TouK/sputnik/saas/sputnik-ci.sh)
{code}
Podpis: .travis.yml
Fill GitHub username as connector.project and GitHub repository name as connector.repository in sputnik.properties
{code - boldem wartości properties connector.project i connector.repo}
project.build.tool=gradle
connector.type=saas
connector.host=sputnik.touk.pl
connector.path=/
connector.port=80
connector.username=
connector.password=
connector.useHttps=false
connector.project=lordOfSputnik
connector.repository=sputnik-test
checkstyle.enabled=true
checkstyle.configurationFile=checkstyle.xml
checkstyle.propertiesFile=
pmd.enabled=false
pmd.ruleSets=rulesets/java/android.xml,rulesets/java/basic.xml
findbugs.enabled=true
findbugs.includeFilter=
findbugs.excludeFilter=
codenarc.enabled=true
codenarc.ruleSets=
codenarc.excludes=**/*.java
{code}
Podpis: sputnik.properties
Add checkstyle.xml

Build Project and read Sputnik comments
---------------------------------------
On every pull-request Sputnik initiates analyses of code that has been changed since the previous build.
If any Sputnik rule - i.e. Checkstyle, PMD, FindBugs, Scalastyle, Code narc or JSLint - is violated you should expect to see comments in GitHub:
6_sputnik_rules_violated_comment.png
You will be also shown a summary of Sputnik analysis:
6_sputnik_rules_violated_summary.png
and receive email notifications.
When Sputnik does not detect any further violations summary looks like this:
6_sputnik_rules_approved.png
