#!/usr/bin/python

import logging, os, subprocess, sys, urllib, zipfile

# variables initiated from ci service env variables
ci = ''
ci_name = ''
pull_request_number = ''
repo_slug = ''
api_key = ''


def configure_logger():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(levelname)s] %(asctime)s %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)


def get_env(single_env):
    try:
        assert (os.environ[single_env])
        return os.environ[single_env]
    except Exception:
        logging.debug("Problem while reading env variable: " + single_env)
        return None


def detect_ci_service():
    global ci_name
    if get_env('TRAVIS'):
        ci_name = 'TRAVIS'
    elif get_env('CIRCLECI'):
        ci_name = 'CIRCLECI'
    logging.debug('Detected ci: ' + ci_name)


def check_required_env_variables(required_vars):
    logging.info("Check required env variables: " + str(required_vars))
    for env_var in required_vars:
        if get_env(env_var) is None:
            logging.error("Env variable " + env_var + " is required to run sputnik")
            return False
    return True


def is_set_every_required_env_variable():
    logging.info('***************** ' + ci_name)
    required_vars = {
        'TRAVIS' : ["CI", "TRAVIS", "TRAVIS_PULL_REQUEST", "TRAVIS_REPO_SLUG"],
        'CIRCLECI': ["CI", "CIRCLECI", "CIRCLE_PROJECT_USERNAME", "CIRCLE_PROJECT_REPONAME", "CI_PULL_REQUEST", "CIRCLE_PR_NUMBER"]
    }
    return check_required_env_variables(required_vars[ci_name])


def init_travis_variables():
    global ci
    ci = get_env("CI")
    global ci_name
    ci_name = get_env("TRAVIS")
    global pull_request_number
    pull_request_number = get_env("TRAVIS_PULL_REQUEST")
    global repo_slug
    repo_slug = get_env("TRAVIS_REPO_SLUG")


def init_circleci_variables():
    global ci
    ci = get_env("CI")
    global ci_name
    ci_name = get_env("CIRCLECI")
    global pull_request_number
    pull_request_number = get_env("CIRCLE_PR_NUMBER")
    global repo_slug
    repo_slug = get_env("CIRCLE_PROJECT_USERNAME") + '/' + get_env("CIRCLE_PROJECT_REPONAME")


def init_variables():
    detect_ci_service()
    if ci_name == 'TRAVIS':
        init_travis_variables()
    elif ci_name == 'CIRCLECI':
        init_circleci_variables()

    global api_key
    api_key = get_env("api_key")


def is_pull_request_initiated():
    if ci == 'true' and ci_name == 'true' and pull_request_number != "false":
        return True
    else:
        logging.warn("Stop continuous integration. Check evn variables CI: " + ci
                     + ", ci name: " + ci_name + ", pull request number: " + pull_request_number)
        return False


def unzip(zip):
    zip_ref = zipfile.ZipFile(zip, 'r')
    zip_ref.extractall(".")
    zip_ref.close()


def download_file(url, file_name):
    logging.info("Downloading " + file_name)
    try:
        urllib.urlretrieve(url, filename=file_name)
    except Exception:
        logging.error("Problem while downloading " + file_name + " from " + url)


def download_files_and_run_sputnik():
    if is_pull_request_initiated():
        if api_key:
            configs_url = "http://sputnik.touk.pl/conf/" + repo_slug + "/configs?key=" + api_key
            download_file(configs_url, "configs.zip")
            unzip("configs.zip")

        sputnik_jar_url = "http://repo1.maven.org/maven2/pl/`touk/sputnik/1.6.0/sputnik-1.6.0-all.jar"
        download_file(sputnik_jar_url, "sputnik.jar")

        subprocess.call(['java', '-jar', 'sputnik.jar', '--conf', 'sputnik.properties', '--pullRequestId', pull_request_number])


def sputnik_ci():
    configure_logger()
    init_variables()

    if is_set_every_required_env_variable():
        download_files_and_run_sputnik()


sputnik_ci()
