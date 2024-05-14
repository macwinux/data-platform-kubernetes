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
    Despliega Redpanda en Kubernetes utilizando Helm.
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
        

        subprocess.run(["helm", "install", "redpanda", "redpanda/redpanda", "--namespace", namespace, "--values", "values-redpanda.yaml"], check=True)
        click.echo("Despliegue de Redpanda completado con éxito!")
    except subprocess.CalledProcessError as e:
        click.echo(f"Error: {e}")
        click.echo("El despliegue de Redpanda ha fallado. Por favor, revisa los mensajes de error.")

if __name__ == '__main__':
    redpanda()
