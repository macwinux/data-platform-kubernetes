import click
import utils.subprocess_com as utils
import sparkop.argu as argu
from os import path
from pathlib import Path

@click.group()
def sparkop():
    """
        Install spark operator command
    """

@sparkop.command(name='install')
def install():
    """Install spark operator in kubernetes
    """
    utils.create_ns('spark-operator')
    utils.create_ns('spark-jobs')
    utils.add_repo('spark-operator', argu.HELM_REPO)
    spark_op = 'spark-operator/spark-operator'
    """The spark operator chart helm points to an image that is not found in the kubeflow/spark-operator registry for now.
    So the version of the image in the resources/sparkop-values.yaml is modified with the correct version."""
    utils.install_repo('spark-operator', 'spark-operator', spark_op, 'sparkop-values.yaml')

@sparkop.command(name="delete")
def delete():
    """Uninstall spark operator from kubernetes
    """
    utils.uninstall_repo('spark-operator', 'spark-operator')
    utils.delete_repo('spark-operator')
    utils.delete_ns('spark-operator')
    utils.delete_ns('spark-jobs')

@sparkop.command(name="revision")
def status():
    """Check the revision for this installation
    """
    utils.run_helm_revision('spark-operator')
    

#@sparkop.command(name="deploy-test")
#@click.argument('app_yaml', type=str, required=True)
#def deploy_test(app_yaml: str):
#    """Deploy an app using spark operator in kubernetes
#
#    Args:
#        app_yaml (str, required): name of the yaml file where the spark is defined. It should be saved in resources directory.
#    """
#    
#    absolute = str(Path(__file__).parent.parent)
#    values_path = path.join(absolute, 'resources', app_yaml)
#    command = ["kubectl", "--namespace", "redpanda", "exec", "-i", "-t", "redpanda-0", "-c", "redpanda", "--", "rpk", "topic", "create", "flink_input"]
#    result = utils.__run_subprocess(command)
#    
#    if result.returncode != 0:
#        click.echo('-------------------------------------------')
#        click.echo(f'Failed creating the topic "flink_input"')
#        click.echo(f'Error: {result.stderr}')
#        click.echo('-------------------------------------------')
#        raise SystemError(result.stderr)
#    else:
#        click.echo('-------------------------------------------')
#        click.echo(f'Topic "flink_input" created!')
#        click.echo('-------------------------------------------')
#    
#    command = ["kubectl", "--namespace", "redpanda", "exec", "-i", "-t", "redpanda-0", "-c", "redpanda", "--", "rpk", "topic", "create", "flink_output"]
#    result = utils.__run_subprocess(command)
#    
#    if result.returncode != 0:
#        click.echo('-------------------------------------------')
#        click.echo(f'Failed creating the topic flink_output')
#        click.echo(f'Error: {result.stderr}')
#        click.echo('-------------------------------------------')
#        raise SystemError(result.stderr)
#    else:
#        click.echo('-------------------------------------------')
#        click.echo(f'Topic flink_output created!')
#        click.echo('-------------------------------------------')
#    
#    command = ["kubectl", "create", "-f", values_path, "--namespace", "spark-jobs"]
#    result = utils.__run_subprocess(command)
#    if result.returncode != 0:
#        click.echo('-------------------------------------------')
#        click.echo(f'Failed deploying the operator {app_yaml}')
#        click.echo('-------------------------------------------')  
#        raise SystemError(result.stderr)
#    else:
#        click.echo('-------------------------------------------')
#        click.echo(f'{app_yaml} installed')
#        click.echo('-------------------------------------------')
#        return result