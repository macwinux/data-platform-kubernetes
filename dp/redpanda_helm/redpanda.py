import click
import subprocess
import yaml
import utils.subprocess_com as utils
import pkg_resources
from pathlib import Path

@click.group()
def redpanda():
    """
    Install redpanda helm chart commad
    """
    pass

@redpanda.command()
@click.option('--tls', '-t', default='false', help='Set TLS configuration in Redpanda')
@click.option('--version', '-v', default='5.8.5', help='Redpanda helm chat version')
@click.option('--namespace', '-n', default='default', help='Namespace where redpanda will be deployed')
@click.option('--brokers', '-b', default=1, help="How many pod replicas (redpanda brokers) will be deployed")

def install(tls: str,  version: str, namespace: str, brokers: str):
    """Deploy Redpanda on Kubernetes using Helm.

    Args:
        tls_enabled (str, optional): Install redpanda using LS (Transport Layer Security) for encrypted communication. Use false to avoid cofigure tls. Defaults to "false".
        version (str, optional): Install the redpanda helm chart with the version specified. Defaults to "5.8.5".
        namespace (str, optional): Install the redpanda cluster in the namespace specified. Defaults to "default".
        brokers (int, optional): How many Pod replicas (Redpanda brokers) will be deployed. Defaults to 1.
    """
    utils.create_ns(namespace)
    utils.add_repo('redpanda', "https://charts.redpanda.com")
    if tls.lower() == 'false':
            data = {
                'tls': {
                    'enabled': False
                },
                "statefulset": {
                    "replicas": brokers
                }
            }
            with open('resources/values-redpanda.yaml', 'w') as file:
                yaml.dump(data, file, default_flow_style=False)
        
    utils.install_repo(namespace, 'redpanda', 'redpanda/redpanda', "values-redpanda.yaml")
    
@redpanda.command()
@click.option('--namespace', '-n', default='default', help='Namespace where redpanda will be deleted')
def delete(namespace):
    """Delete Redpanda in Kubernetes using Helm

    Args:
        namespace (str,optional): Delete the redpanda cluster in the namespace specified. Defaults set to 'default'
    """
    utils.uninstall_repo('redpanda', 'redpanda')
    
    #Al borrar el repo siguen quednao un pod de configuración y un job dentro del namespace donde se depliega redpanda que hay que borrar manualmente. Tmabién queda los pvc si son configurados.
    try:   
        click.echo(f"kubectl delete pod --all --namespace {namespace}")
        subprocess.run(["kubectl", "delete", "pod", "--all","--namespace", namespace], check=True)
        
        click.echo(f"kubectl delete pvc --all --namespace {namespace}")
        subprocess.run(["kubectl", "delete", "secret", "--all","--namespace", namespace], check=True)
        
        click.echo(f"kubectl delete job redpanda-configuration --namespace {namespace}")
        subprocess.run(["kubectl", "delete", "job", "redpanda-configuration","--namespace", namespace], check=True)
    except subprocess.CalledProcessError as e:
        click.echo(f"Error: {e}")
        click.echo("Redpanda deletion has failed. Please check the error messages.")
    
    utils.delete_repo('redpanda')
    utils.delete_ns('redpanda')

if __name__ == '__main__':
    redpanda()
