#import argparse
import subprocess
import click
import argu
#parser = argparse.ArgumentParser(description='flink operator arguments')
#parser.add_argument('version', type=str, help='Flink operator version to install. Default last version 1.19',
#                    default='1.8.0')
#
#args = parser.parse_args()
#
#helm_command = 'helm repo add flink-operator-repo https://downloads.apache.org/flink/flink-kubernetes-operator-' + args.version
#
##Check the arguments passed
#print()
#print('Argument values: ')
#print(args.version)
#print('helm command: ' + helm_command)
#
#helm_return = subprocess.run(helm_command, shell=True, capture_output=True)
#
#print('Helm code output: ' + str(helm_return.returncode))
#print(helm_return)


@click.group()
def flinkop():
    """
        Install flink operator command
    """

@flinkop.command(name='install')
@click.argument('v', type=str)
def install(v: str='1.8.0'):
    """

    Args:
        v (str, optional): _description_. Defaults to '1.8.0'.
    Install the flink operator with helm with the version specified.
    
    """
    
    #Create namespaces
    flink_op_ns = subprocess.run(['kubectl', 'create', 'ns', 'flink-operator'])
    
    if flink_op_ns.returncode == 0: 
        click.echo('-------------------------------------------')
        click.echo('flink-operator namespace created')
        click.echo('-------------------------------------------')
        flink_jobs_ns = subprocess.run(['kubectl', 'create', 'ns', 'flink-jobs'])
    else:
        click.echo('-------------------------------------------')
        click.echo('Failed creating the flin-operator namespace')
        click.echo('-------------------------------------------')
        click.echo('Command: ' + str(flink_op_ns.args))
        return 0
    
    if flink_jobs_ns.returncode == 0:
        click.echo('-------------------------------------------')
        click.echo('flink-jobs namespace created')
        click.echo('-------------------------------------------')
        helm_command = ['helm', 'repo', 'add', 'flink-operator-repo', argu.HELM_REPO + v]
        click.echo('helm command: ' + str(helm_command))
        helm_return = subprocess.run(helm_command, shell=True, capture_output=True)
        click.echo(helm_return)
    else:
        click.echo('-------------------------------------------')
        click.echo('Failed creating the flin-jobs namespace')
        click.echo('-------------------------------------------')
        click.echo('Command: ' + str(flink_jobs_ns.args))
        return 0

    if helm_return.returncode==0:
        click.echo('-------------------------------------------')
        click.echo('Flink Operator added to Helm')
        click.echo('-------------------------------------------')
        flink_op = f'flink-kubernetes-operator-{v}/flink-kubernetes-operator'
        install_command = ['helm', '-n', 'flink-operator', 'install', '-f',
                           'values.yaml' , flink_op, '--set', 'webhook.create=false']
        install_return = subprocess.run(install_command, shell=True, capture_output=True)
        click.echo(install_return)
    else:
        click.echo('-------------------------------------------')
        click.echo('Error creating the flink operator in Kubernetes')
        click.echo('-------------------------------------------')
        click.echo(helm_return.stderr)
        click.echo('-------------------------------------------')
        return 0
    if install_return.returncode==0:
        click.echo('-------------------------------------------')
        click.echo('Flink Operator created')
        click.echo('-------------------------------------------')

if __name__ == '__main__':
    flinkop()