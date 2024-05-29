
import click
import utils.subprocess_com as utils
import flinkop.argu as argu
from os import path
from pathlib import Path


@click.group()
def flinkop():
    """
        Install flink operator command
    """

@flinkop.command(name='install')
@click.argument('v', type=str, required=False, default='1.8.0')
def install(v: str):
    """Install flink operator in kubernetes

    Args:
        v (str, optional): version that you want to install in kubernetes Defaults to '1.8.0'.
    
    """
    utils.create_ns('flink-operator')
    utils.create_ns('flink-jobs')
    utils.add_repo('flink-operator', argu.HELM_REPO+v)
    flink_op = 'flink-operator/flink-kubernetes-operator'
    utils.install_repo('flink-operator', 'flink-operator', flink_op, "flinkop-values.yaml")
    
@flinkop.command(name="delete")
def delete():
    """Uninstall flink operator from kubernetes
    """
    utils.uninstall_repo('flink-operator', 'flink-operator')
    utils.delete_repo('flink-operator')
    utils.delete_ns('flink-operator')
    utils.delete_ns('flink-jobs')

@flinkop.command(name="deploy-test")
@click.option('--namespace', '-n', default='default', help='Namespace where app is deployed')
@click.argument('app_yaml', type=str, required=True)
def deploy_test(app_yaml: str, namespace):
    """Deploy an app using flink operator in kubernetes

    Args:
        app_yaml (str): _description_
        namespace (_type_): _description_
    """
    absolute = str(Path(__file__).parent.parent)
    values_path = path.join(absolute, 'resources', app_yaml)
    command = ["kubectl", "create", "-f", values_path, "--namespace", namespace]
    result = utils.run_subprocess(command)
    if result.returncode != 0:
        click.echo('-------------------------------------------')
        click.echo(f'Failed deploying the operator {app_yaml}')
        click.echo('-------------------------------------------')  
        raise SystemError(result.stderr)
    else:
        click.echo('-------------------------------------------')
        click.echo(f'{app_yaml} installed')
        click.echo('-------------------------------------------')
        return result