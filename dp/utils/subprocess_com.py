#from pathlib import Path
#import pkg_resources
import click
from subprocess import CompletedProcess, run
import sys
from os import path
from pathlib import Path

def create_ns(namespace: str)-> CompletedProcess[bytes]:
    """ Command that create a new namespace in kubernetes

    Args:
        namespace (str): kubernetes namespace

    Raises:
        SystemError: return a SystemError if kubectl command fails

    Returns:
        CompletedProcess[bytes]: return a class that contains some fields: args, returncode, stderr, stdout
    """
    
    create_ns = ['kubectl', 'create', 'ns', namespace]
    result = run_subprocess(create_ns)
    
    if result.returncode != 0:
        click.echo('-------------------------------------------')
        click.echo(f'Failed creating the namespace: {namespace}')
        click.echo('-------------------------------------------')
        raise SystemError(result.stderr)
    else:
        click.echo('-------------------------------------------')
        click.echo(f'{namespace} namespace created')
        click.echo('-------------------------------------------')
        return result 

def delete_ns(namespace: str) -> CompletedProcess[bytes]:
    """Command that delete a namespace in kubernetes

    Args:
        namespace (str): kubernetes namespace

    Returns:
        CompletedProcess[bytes]: return a class that contains some fields: args, returncode, stderr, stdout
    """
    delete_ns = ['kubectl', 'delete', 'ns', namespace]
    result = run_subprocess(delete_ns)
    
    if result.returncode != 0:
        click.echo('-------------------------------------------')
        click.echo(f'Failed deleting the namespace: {namespace}')
        click.echo('-------------------------------------------')
        raise SystemError(result.stderr)
    else:
        click.echo('-------------------------------------------')
        click.echo(f'{namespace} namespace deleted')
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

def delete_repo(repo_name: str) -> CompletedProcess[bytes]:
    """Command that remove a repository in helm

    Args:
        repo_name (str): name of the repo in helm

    Returns:
        CompletedProcess[bytes]: return a class that contains some fields: args, returncode, stderr, stdout
    """
    helm_command = ['helm', 'repo', 'remove', repo_name]
    result = run_subprocess(helm_command)
    if result.returncode != 0:
        click.echo('-------------------------------------------')
        click.echo(f'Failed removing the repository {repo_name}')
        click.echo('-------------------------------------------')  
        raise SystemError(result.stderr)
    else:
        click.echo('-------------------------------------------')
        click.echo(f'{repo_name} removed')
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
    #path = pkg_resources.resource_filename("dp","resources")
    #values_path = next(Path(path).glob(values_yaml), values_yaml)
    absolute = str(Path(__file__).parent.parent)
    values_path = path.join(absolute, 'resources', values_yaml)
    
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

def uninstall_repo(namespace: str, operator_name: str) -> CompletedProcess[bytes]:
    """Command for uninstall all teh components intalled by a repo helm
    
    Args:
        namspace (str): name of the namespace in kubernetes that contains the repo components installed
        repo_name (str): name of the repo in helm
        operator_name (str): operator from the repo that you want to install
        
    Returns:
        CompletedProcess[bytes]: return a class that contains some fields: args, returncode, stderr, stdout
    """
    uninstall_command = ['helm', 'uninstall', operator_name,'-n',namespace]
    result = run_subprocess(uninstall_command)
    if result.returncode != 0:
        click.echo('-------------------------------------------')
        click.echo(f'Failed uninstaling the operator {operator_name}')
        click.echo('-------------------------------------------')  
        raise SystemError(result.stderr)
    else:
        click.echo('-------------------------------------------')
        click.echo(f'{operator_name} uninstalled')
        click.echo('-------------------------------------------')
        return result  

def run_subprocess(commands: list, input: str = None) -> CompletedProcess[bytes]:
    """run a subprocess in the operating system

    Args:
        commands (list): list of command to run in the operating system.

    Returns:
        CompletedProcess[bytes]: return a class that contains some fields: args, returncode, stderr, stdout
    """
    #This block if else is to check if the run command exectued by the redpanda prodcuce message function. This function send a message in input parameter.
    if input == None:
        result = run(commands, shell=True, capture_output=True)
    else:
        result = run(commands, shell=True, capture_output=True, input=bytes(input,'utf-8'))

    return result 


def run_kubectl_delete(resource_type: str, namespace: str, resource_name: str = "--all") -> CompletedProcess[bytes]:
    """Helper function to run kubectl delete commands and handle errors.

    Args:
        resource_type (str): _description_
        namespace (str): _description_
        resource_name (str, optional): _description_. Defaults to "--all".

    Raises:
        SystemError: _description_
    """
    delete_command = ["kubectl", "delete", resource_type, resource_name, "--namespace", namespace]
    result = run_subprocess(delete_command)
    
    if result.returncode != 0:
        click.echo('-------------------------------------------')
        click.echo(f'Failed deleting the {resource_type} {resource_name} in namespace {namespace}')
        click.echo(f'Error: {result.stderr}')
        click.echo('-------------------------------------------')
        raise SystemError(result.stderr)
    else:
        click.echo('-------------------------------------------')
        click.echo(f' {resource_type} {resource_name} in {namespace} deleted')
        click.echo('-------------------------------------------')
        return result
    