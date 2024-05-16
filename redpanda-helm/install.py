import click
import subprocess
import yaml

@click.group()
def redpanda():
    """
    Script para desplegar el chart de Redpanda utilizando Helm.
    """
    pass

@redpanda.command()
@click.argument('tls_enabled')
@click.option('--version', default='5.8.5', help='Redpanda helm chat version')
@click.option('--namespace', '-n', default='default', help='Namespace where redpanda will be deployed')
@click.option('--brokers', '-b', default=1, help="How many Pod replicas (Redpanda brokers) will be deployed")

def install(tls_enabled="false", version="5.8.5", namespace="default", brokers=1):
    """
    Deploy Redpanda on Kubernetes using Helm.
        Args:
        tls_enaled (str, mandatory): _description_. Defaults 'false'.
        Install redpanda using LS (Transport Layer Security) for encrypted communication. Use false to avoid cofigure tls. Defaults 'false'.
        

        Options:
        --version (str, optional): _description_. Defaults to '5.8.5'.
        Install the redpanda helm chart with the version specified.
        
        --namespace (str, optional): _description_. Defaults to 'default'.
        Install the redpanda cluster in the namespace specified

        --brokers (str, optional): _description_. Defaults to 1.
        How many Pod replicas (Redpanda brokers) will be deployed.. Defaults to 1-
    """
    try:
        # Agregar el repositorio de Helm de Redpanda
        subprocess.run(["helm", "repo", "add", "redpanda", "https://charts.redpanda.com"], check=True)
        subprocess.run(["helm", "repo", "update"], check=True)
        
        # Crear el namespace si no existe
        namespace_exists = subprocess.run(["kubectl", "get", "namespace", namespace], capture_output=True, text=True)
        if namespace_exists.returncode != 0:
            # El namespace no existe, crearlo
            click.echo(f"kubectl create namespace --namespace {namespace}")
            subprocess.run(["kubectl", "create", "namespace", namespace], check=True)
        
        if tls_enabled.lower() == 'false':
            data = {
                'tls': {
                    'enabled': False
                },
                "statefulset": {
                    "replicas": brokers
                }
            }
            with open('values-redpanda.yaml', 'w') as file:
                yaml.dump(data, file, default_flow_style=False)
        
        click.echo(f"helm install redpanda redpanda/redpanda --namespace {namespace} --values values-redpanda.yaml")
        subprocess.run(["helm", "install", "redpanda", "redpanda/redpanda", "--namespace", namespace, "--values", "values-redpanda.yaml"], check=True)
        click.echo("Redpanda deployment completed successfully!")
    except subprocess.CalledProcessError as e:
        click.echo(f"Error: {e}")
        click.echo("Redpanda deployment has failed. Please check the error messages.")


@redpanda.command()
@click.option('--namespace', '-n', default='default', help='Namespace where redpanda will be deleted')
def delete(namespace):
    """
    Delete Redpanda in Kubernetes using Helm.
    
    Options:    
    --namespace (str, optional): _description_. Defaults to 'default'.
        Delete the redpanda cluster in the namespace specified
    """
    try:
        click.echo(f"helm uninstall redpanda --namespace {namespace}")
        subprocess.run(["helm", "uninstall", "redpanda", "--namespace", namespace], check=True)
        
        click.echo(f"kubectl delete pod --all --namespace {namespace}")
        subprocess.run(["kubectl", "delete", "pod", "--all","--namespace", namespace], check=True)
        
        click.echo(f"kubectl delete pvc --all --namespace {namespace}")
        subprocess.run(["kubectl", "delete", "secret", "--all","--namespace", namespace], check=True)
        
        click.echo(f"kubectl delete job redpanda-configuration --namespace {namespace}")
        subprocess.run(["kubectl", "delete", "job", "redpanda-configuration","--namespace", namespace], check=True)
    except subprocess.CalledProcessError as e:
        click.echo(f"Error: {e}")
        click.echo("Redpanda deletion has failed. Please check the error messages.")

if __name__ == '__main__':
    redpanda()
