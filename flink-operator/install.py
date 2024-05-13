#import argparse
import subprocess
import click
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
    
    click.echo('Version of flink-operator: ' + v)
    helm_command = 'helm repo add flink-operator-repo https://downloads.apache.org/flink/flink-kubernetes-operator-' + v
    click.echo('helm command: ' + helm_command)

if __name__ == '__main__':
    flinkop()