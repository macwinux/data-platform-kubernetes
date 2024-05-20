from pathlib import Path
import click
from subprocess import CompletedProcess, run
import pkg_resources

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
        click.echo(f'{namespace} namespace created')
        click.echo('-------------------------------------------')
        return result 


def add_repo(repo_name: str, repo_url: str) -> CompletedProcess[bytes]:
    """Command that add a new repository in helm

    Args:
        repo_name (str): nick for the repo that you're adding in helm
        repo_url (str): url that point to the helm repository 

    Raises:
        SystemError: Error if the repo add fails

    Returns:
        CompletedProcess[bytes]: return a class that contains some fields: args, returncode, stderr, stdout
    """
    helm_command = ['helm', 'repo', 'add', repo_name, repo_url]
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


def install_repo(namespace: str, repo_name:str, operator_name: str, values_yaml: str) -> CompletedProcess[bytes]:
    """Command for install a repo added in Helm

    Args:
        namespace (str): name of the namespace in kubernetes
        repo_name (str): name of the repo in helm
        operator_name (str): operator that you want to install in helm

    Raises:
        SystemError: Error if the repo install fails
    Returns:
        CompletedProcess[bytes]: return a class that contains some fields: args, returncode, stderr, stdout
    """
    path = pkg_resources.resource_filename("dp","resources")
    values_path = next(Path(path).glob(values_yaml), values_yaml)
    install_command = ['helm', '-n', namespace, 'install', '-f',
                           values_path , repo_name, operator_name, '--set', 'webhook.create=false']
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