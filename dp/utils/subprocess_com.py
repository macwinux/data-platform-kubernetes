#from pathlib import Path
#import pkg_resources
import time
import click
from subprocess import CompletedProcess, run, Popen, PIPE
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
    result = __run_subprocess(create_ns)
    return __print_output(result=result,ok_msg=[f'{namespace} namespace created'], fail_msg=[f'Failed creating the namespace: {namespace}'])

def delete_ns(namespace: str) -> CompletedProcess[bytes]:
    """Command that delete a namespace in kubernetes

    Args:
        namespace (str): kubernetes namespace

    Returns:
        CompletedProcess[bytes]: return a class that contains some fields: args, returncode, stderr, stdout
    """
    delete_ns = ['kubectl', 'delete', 'ns', namespace]
    result = __run_subprocess(delete_ns)
    return __print_output(result=result,ok_msg=[f'{namespace} namespace deleted'], fail_msg=[f'Failed deleting the namespace: {namespace}'])

def update_helm():
    """Command that update helm
    """
    helm_command = ['helm', 'repo', 'update']
    result = __run_subprocess(helm_command)
    return __print_output(result=result,ok_msg=['helm repo updated'], fail_msg=['Failed updating helm'])

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
    result = __run_subprocess(helm_command)
    return __print_output(result=result,ok_msg=[f'{repo_name} added'], fail_msg=[f'Failed adding the repository {repo_name}'])

def delete_repo(repo_name: str) -> CompletedProcess[bytes]:
    """Command that remove a repository in helm

    Args:
        repo_name (str): name of the repo in helm

    Returns:
        CompletedProcess[bytes]: return a class that contains some fields: args, returncode, stderr, stdout
    """
    helm_command = ['helm', 'repo', 'remove', repo_name]
    result = __run_subprocess(helm_command)
    return __print_output(result=result,ok_msg=[f'{repo_name} removed'], fail_msg=[f'Failed removing the repository {repo_name}'])


def install_repo(namespace: str, repo_name:str, operator_name: str, values_yaml: str = None) -> CompletedProcess[bytes]:
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
    if values_yaml is not None:
        absolute = str(Path(__file__).parent.parent)
        values_path = path.join(absolute, 'resources', values_yaml)
        install_command = ['helm', '-n', namespace, 'install', '-f',
                           values_path , repo_name, operator_name]
    else:
        install_command = ['helm', '-n', namespace, 'install', repo_name, operator_name]

    result = __run_subprocess(install_command)
    return __print_output(result=result,ok_msg=[f'{repo_name} installed'], fail_msg=[f'Failed instaling the repository {repo_name}'])

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
    result = __run_subprocess(uninstall_command)
    return __print_output(result=result,ok_msg=[f'{operator_name} uninstalled'], fail_msg=[f'Failed uninstaling the operator {operator_name}'])

def run_kubectl_apply(resource_yaml: str, namespace: str = None) -> CompletedProcess[bytes]:
    """Helper function to run kubectl apply commands froma  file or url

    Args:
        resource_yaml (str): yaml file that you want to run

    Returns:
        CompletedProcess[bytes]: return a class that contains some fields: args, returncode, stderr, stdout
    """
    if namespace is not None:
        absolute = str(Path(__file__).parent.parent)
        resource_path = path.join(absolute, 'resources', resource_yaml)
        command = ["kubectl", "apply", '-f', resource_path, "--namespace", namespace]
        result = __run_subprocess(command)
        return __print_output(result=result,ok_msg=[f' Applying the file {resource_yaml}'], fail_msg=[f'Failed applying the file {resource_yaml}',f'Error: {result.stderr}'])
    else:
        absolute = str(Path(__file__).parent.parent)
        resource_path = path.join(absolute, 'resources', resource_yaml)
        command = ["kubectl", "apply", '-f', resource_path]
        result = __run_subprocess(command)
        return __print_output(result=result,ok_msg=[f' Applying the file {resource_yaml}'], fail_msg=[f'Failed applying the file {resource_yaml}',f'Error: {result.stderr}'])

def run_kubectl_delete_with_res(resource_type: str, namespace: str, resource_name: str = "--all") -> CompletedProcess[bytes]:
    """Helper function to run kubectl delete commands and handle errors.

    Args:
        resource_type (str): kind of resource that you want to delete
        namespace (str): namespace where is the resource
        resource_name (str, optional): name of the resource that you want to delete
    
    Returns:
        CompletedProcess[bytes]: return a class that contains some fields: args, returncode, stderr, stdout
    """
    delete_command = ["kubectl", "delete", resource_type, resource_name, "--namespace", namespace]
    result = __run_subprocess(delete_command)
    return __print_output(result=result,ok_msg=[f' {resource_type} {resource_name} in {namespace} deleted'], 
                   fail_msg=[f'Failed deleting the {resource_type} {resource_name} in namespace {namespace}',f'Error: {result.stderr}'])
 
def run_kubectl_delete(resource_yaml:str, namespace: str = None) -> CompletedProcess[bytes]:
    """Helper function to run kubectl delete commands and handle errors.

    Args:
        resource_yaml (str): yaml file that contains the service that you want to delete
    
    Returns:
        CompletedProcess[bytes]: return a class that contains some fields: args, returncode, stderr, stdout
    """
    if namespace is not None:
        absolute = str(Path(__file__).parent.parent)
        resource_path = path.join(absolute, 'resources', resource_yaml)
        delete_command = ["kubectl", "delete", "-f", resource_path, "--namespace", namespace]
        result = __run_subprocess(delete_command)
        return __print_output(result=result,ok_msg=[f'{resource_yaml} deleted'], 
                    fail_msg=[f'Failed deleting resource: {resource_yaml}',f'Error: {result.stderr}'])
    else:
        absolute = str(Path(__file__).parent.parent)
        resource_path = path.join(absolute, 'resources', resource_yaml)
        delete_command = ["kubectl", "delete", "-f", resource_path]
        result = __run_subprocess(delete_command)
        return __print_output(result=result,ok_msg=[f'{resource_yaml} deleted'], 
                    fail_msg=[f'Failed deleting resource: {resource_yaml}',f'Error: {result.stderr}'])

def run_helm_revision(namespace: str) -> CompletedProcess[bytes]:
    """Return revision name of the repo deployed

    Args:
        namespace (str): repo that you want to check

    Returns:
        CompletedProcess[bytes]: return a class that contains some fields: args, returncode, stderr, stdout
    """
    status_command = ['helm', 'list', '-n', namespace]
    result = __run_subprocess(status_command)
    return __print_output(result=result, ok_msg=[result.stdout], fail_msg=[f'Failed'])

def apply_cert_manager():
    """install the cert manager in case it is not installed.
    """
    command = ['kubectl', 'get', 'pods', '-n', 'cert-manager']
    result = __run_subprocess(commands=command)
    if result.returncode != 0 or b'No resources found in cert-manager namespace' in result.stderr:
        click.echo('-------------------------------------------')
        click.echo('cert-manager is not installed. Installing...')
        click.echo('-------------------------------------------')
        run_kubectl_apply('cert-manager.yaml')
        click.echo("-------------------------------------------")
        click.echo("Waiting for cert-manager being up and running.")
        click.echo("-------------------------------------------")
        time.sleep(120)
    else:
        click.echo('-------------------------------------------')
        click.echo('cert-manager already installed')
        click.echo('-------------------------------------------')

def __run_subprocess(commands: list, input: str = None, capture: bool = True) -> CompletedProcess[bytes]:
    """run a subprocess in the operating system

    Args:
        commands (list): list of command to run in the operating system.

    Returns:
        CompletedProcess[bytes]: return a class that contains some fields: args, returncode, stderr, stdout
    """
    #This block if else is to check if the run command exectued by the redpanda prodcuce message function. This function send a message in input parameter.
    if input == None:
        result = run(commands, shell=True, capture_output=capture)
    else:
        result = run(commands, shell=True, capture_output=capture, input=bytes(input,'utf-8'))

    return result

def __run_Popen(commands: list, text=True) -> None:
    """run a Popen subprocess in the operating system

    Args:
        commands (list): list of command to run in the operating system.
        text (boolean): It specifies whether the input and output streams of the process should be text (True). False to handle inputs and outputs as byte sequences.

    """
    process = Popen(commands, stdout=PIPE, stderr=PIPE, text=text)
    try:
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
    finally:
        process.stdout.close()
        process.stderr.close()
 

def __print_output(result: CompletedProcess[bytes], ok_msg: list[str], fail_msg: list[str]) -> CompletedProcess[bytes]:
    """Print the output from the result returned by subprocess

    Args:
        result (CompletedProcess[bytes]): result from subprocess
        ok_msg (list[str]): if the result is successful, return message
        fail_msg (list[str]): if the result fails, failed message.

    Raises:
        SystemError: When an error occurs in subprocess command, raise an error after print it.

    Returns:
        CompletedProcess[bytes]: return the result from the subprocess.
    """
    ok_error_list = ['(AlreadyExists)', '(NotFound)', 'no repositories configured']
    for msg in ok_error_list:
        if result.returncode == 1 and msg in str(result.stderr):
            click.echo('-------------------------------------------')
            click.echo(str(result.stderr).split(':', 1)[1].split('\\')[0])
            click.echo('-------------------------------------------')
            return result
    if result.returncode != 0:
        click.echo('-------------------------------------------')
        for msg in fail_msg:
            click.echo(msg)
        click.echo('-------------------------------------------')
        raise SystemError(result.stderr)
    else:
        for msg in ok_msg:
            click.echo('-------------------------------------------')
            click.echo(msg)
            click.echo('-------------------------------------------')
        return result