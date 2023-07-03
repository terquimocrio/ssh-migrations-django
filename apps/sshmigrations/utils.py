import paramiko
import requests
import logging


def get_all_branches_as_tuple(repo_owner, repo_name, access_token):

    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/branches'

    headers = {'Authorization': f'token {access_token}'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:

        logging.info(f"Successfully retrieved branches. {response.json()}")

        branches = [(branch['name'], branch['name'])
                    for branch in response.json()]
        return branches

    else:
        
        logging.error(f"Error retrieving branches. {response.json()}")

        return None


def ssh_connection(private_key_path, host, port, username):

    client = paramiko.SSHClient()

    private_key = paramiko.RSAKey.from_private_key_file(private_key_path)

    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(host, port, username, pkey=private_key, timeout=10)

    return client


def merge_branch(project_path, branch, connection, main_branch='main'):

    cmd_1 = f"cd {project_path} && source venv/bin/activate && git checkout {main_branch} && git pull origin {main_branch}"
    cmd_2 = f"cd {project_path} && source venv/bin/activate && git checkout {branch} && git pull origin {branch}"
    cmd_3 = f"cd {project_path} && source venv/bin/activate && git checkout {branch} && git merge {main_branch}"
    cmd_4 = f"cd {project_path} && source venv/bin/activate && git checkout {main_branch} && git merge {branch}"

    _stdin, _stdout, _stderr = connection.exec_command(
        f"{cmd_1} && {cmd_2} && {cmd_3} && {cmd_4}")

    return _stdout.read().decode('utf-8'), _stderr.read().decode('utf-8')


def makemigrations(project_path, branch, connection):

    _stdin, _stdout, _stderr = connection.exec_command(
        f"cd {project_path} && source venv/bin/activate && python3 manage.py makemigrations")

    return _stdout.read().decode('utf-8'), _stderr.read().decode('utf-8')


def migrate(proyect_path, branch, connection):

    _stdin, _stdout, _stderr = connection.exec_command(
        f"cd {proyect_path} && source venv/bin/activate && python3 manage.py migrate")

    return _stdout.read().decode('utf-8'), _stderr.read().decode('utf-8')
