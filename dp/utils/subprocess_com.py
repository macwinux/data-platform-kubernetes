import click
from subprocess import CompletedProcess, run


def create_ns(namespace: str)-> CompletedProcess[bytes]:
    """ Command that create a new namespace in kubernetes

    Args:
        namespace (str): kubernetes namespace

    Raises:
        SystemError: return a SystemError if kubectl command fails

    Returns:
        CompletedProcess[bytes]: return a class that contains some fields: args, returncode, stderr, stdout
    """
    
    create_ns_flink_jobs = ['kubectl', 'create', 'ns', namespace]
    result = run_subprocess(create_ns_flink_jobs)
    
    if result.returncode != 0:
        click.echo('-------------------------------------------')
        click.echo(f'Failed creating the {namespace} namespace')
        click.echo('-------------------------------------------')
        raise SystemError(result.stderr)
    else:
        click.echo('-------------------------------------------')
        click.echo('{namespace} namespace created')
        click.echo('-------------------------------------------')
        return result 


def add_repo(repo_name: str, repo_url: str) -> CompletedProcess[bytes]:
    """Command that add a new repository in helm

    Args:
        repo_name (str): nick for the repo that you're adding in helm
        repo_url (str): url that point to the helm repository 

    Raises:
        SystemError: _description_

    Returns:
        CompletedProcess[bytes]: _description_
    """
    helm_command = ['helm', 'repo', 'add', repo_name, repo_url]
    click.echo('helm command: ' + str(helm_command))
    result = run_subprocess(helm_command)
    if result.returncode != 0:
        click.echo('-------------------------------------------')
        click.echo(f'Failed adding the repository {repo_name}')
        click.echo('-------------------------------------------')  
        raise SystemError(result.stderr)
    else:
        click.echo('-------------------------------------------')
        click.echo(f'{repo_name} added')
        click.echo('-------------------------------------------')
        return result  


def install_repo(repo_name:str, operator_name: str) -> CompletedProcess[bytes]:
    install_command = ['helm', '-n', repo_name, 'install', '-f',
                           'values.yaml' , operator_name, '--set', 'webhook.create=false']
    result = run_subprocess(install_command)
    if result.returncode != 0:
        click.echo('-------------------------------------------')
        click.echo(f'Failed instaling the repository {repo_name}')
        click.echo('-------------------------------------------')  
        raise SystemError(result.stderr)
    else:
        click.echo('-------------------------------------------')
        click.echo(f'{repo_name} installed')
        click.echo('-------------------------------------------')
        return result  


def run_subprocess(commands: list) -> CompletedProcess[bytes]:
    """run a subprocess in the operating system

    Args:
        commands (list): list of command to run in the operating system.

    Returns:
        CompletedProcess[bytes]: return a class that contains some fields: args, returncode, stderr, stdout
    """
    result = run(commands, shell=True, capture_output=True)
    return result 