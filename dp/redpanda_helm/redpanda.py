import click
import yaml
import utils.subprocess_com as utils
from os import path
from pathlib import Path

@click.group()
def redpanda():
    """
    Install redpanda helm chart commad
    """
    pass

@redpanda.command()
@click.option('--tls', '-t', default='false', help='Set TLS configuration in Redpanda')
@click.option('--version', '-v', default='5.8.5', help='Redpanda helm chart version')
@click.option('--namespace', '-n', default='redpanda', help='Namespace where redpanda will be deployed')
@click.option('--brokers', '-b', default=1, help="How many replica pods (redpanda brokers) will be deployed")

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
            absolute = str(Path(__file__).parent.parent)
            values_path = path.join(absolute, 'resources', 'values-redpanda.yaml')
            with open(values_path, 'w') as file:
                yaml.dump(data, file, default_flow_style=False)

    utils.install_repo(namespace, 'redpanda', 'redpanda/redpanda', "values-redpanda.yaml")
    
@redpanda.command()
@click.option('--namespace', '-n', default='default', help='Namespace where Redpanda will be deleted')
def delete(namespace):
    """Delete Redpanda in Kubernetes using Helm

    Args:
        namespace (str, optional): Delete the Redpanda cluster in the namespace specified. Defaults to 'default'
    """
    utils.uninstall_repo('redpanda', 'redpanda')

    # Al borrar el repo siguen quedando un pod de configuración y un job dentro del namespace donde se despliega Redpanda que hay que borrar manualmente. También quedan los PVC si son configurados.
    resources_to_delete = [
        ("pod", "--all"),
        ("pvc", "--all"),
        ("secret", "--all"),
        ("job", "redpanda-configuration")
    ]

    for resource_type, resource_name in resources_to_delete:
        utils.run_kubectl_delete_with_res(resource_type=resource_type, namespace=namespace, resource_name=resource_name)
    
    utils.delete_repo('redpanda')
    utils.delete_ns('redpanda')

@redpanda.command()
@click.option('--namespace', '-n', default='default', help='Namespace where redpanda is installed')
@click.argument('topic_name', type=str, required=True)
def create_topic(namespace: str, topic_name: str):
    """Create a topic in Redpanda

    Args:
        namespace (str, optional): Namespace where the Redpanda cluster is created.
        topic_name (str, required): Name of the Topic
    """
    create_command = ["kubectl", "--namespace", namespace, "exec", "-i", "-t", "redpanda-0", "-c", "redpanda", "--", "rpk", "topic", "create", topic_name]
    result = utils.__run_subprocess(create_command)
    
    if result.returncode != 0:
        click.echo('-------------------------------------------')
        click.echo(f'Failed creating the topic {topic_name}')
        click.echo(f'Error: {result.stderr}')
        click.echo('-------------------------------------------')
        raise SystemError(result.stderr)
    else:
        click.echo('-------------------------------------------')
        click.echo(f'Topic {topic_name} created!')
        click.echo('-------------------------------------------')

@redpanda.command()
@click.option('--namespace', '-n', default='default', help='Namespace where redpanda is installed')
@click.argument('topic_name', type=str, required=True)
def delete_topic(namespace: str, topic_name: str):
    """Delete a topic in Redpanda

    Args:
        namespace (str, optional): Namespace where the Redpanda cluster is created.
        topic_name (str, required): Name of the Topic
    """
    delete_command = ["kubectl", "--namespace", namespace, "exec", "-i", "-t", "redpanda-0", "-c", "redpanda", "--", "rpk", "topic", "delete", topic_name]
    result = utils.__run_subprocess(delete_command)
    
    if result.returncode != 0:
        click.echo('-------------------------------------------')
        click.echo(f'Failed deleting the topic {topic_name}')
        click.echo(f'Error: {result.stderr}')
        click.echo('-------------------------------------------')
        raise SystemError(result.stderr)
    else:
        click.echo('-------------------------------------------')
        click.echo(f'Topic {topic_name} deleted!')
        click.echo('-------------------------------------------')

@redpanda.command()
@click.option('--namespace', '-n', default='default', help='Namespace where redpanda is installed')
@click.argument('topic_name', type=str, required=True)
@click.option('--message', '-m', default='default message', help='Message to produce')
@click.option('--count', '-c', default=10, type=int, help='Number of messages to produce')
def produce_messages(namespace: str, topic_name: str, message: str, count: int):
    """Produce CLI messages into a Redpanda topic

    Args:
        namespace (str, optional): namespace where redpanda is running
        topic_name (str, required): topic to send the messages to
        message (str, optional): message to send
        count (int, required): numbers of message repetitions

    Raises:
        SystemError: Error with the stderr from the subprocess
    """
    produce_command = ["kubectl", "--namespace", namespace, "exec", "-i", "-t", "redpanda-0", "-c", "redpanda", "--", "rpk", "topic", "produce", topic_name]
    input_messages = "\n".join([f"{message} {i+1}" for i in range(count)]) + "\n"
  
    result = utils.__run_subprocess(produce_command, input=input_messages)
    
    if result.returncode != 0:
        click.echo('-------------------------------------------')
        click.echo(f'Failed sending messages to topic {topic_name}')
        click.echo(f'Error: {result.stderr}')
        click.echo('-------------------------------------------')
        raise SystemError(result.stderr)
    else:
        click.echo('-------------------------------------------')
        click.echo(f'Messages sent to topic {topic_name}!')
        click.echo('-------------------------------------------')
        
@redpanda.command(name="revision")
@click.option('--namespace', '-n', default='redpanda', help='Namespace where redpanda is installed')
def status(namespace: str):
    """Check the revision for this installation
    """
    utils.run_helm_revision(namespace)