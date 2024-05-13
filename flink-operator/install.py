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


@click.command('install')
@click.argument('v', type=str)
@click.version_option('0.1.0', prog_name='flink-operator')
def install(v: str='1.8.0'):
    click.echo('Version of flink-operator: ' + v)
    helm_command = 'helm repo add flink-operator-repo https://downloads.apache.org/flink/flink-kubernetes-operator-' + v
    click.echo('helm command: ' + helm_command)
if __name__ == '__main__':
    install()