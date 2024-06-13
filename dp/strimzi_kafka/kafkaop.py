import click
import utils.subprocess_com as utils
import strimzi_kafka.argu as argu
from os import path
from pathlib import Path
import yaml
import subprocess

@click.group()
def kafkaop():
    """
        Install strimzi kafka operator command.
    """

@kafkaop.command(name='install')
def install():
    """Install strimzi kafka operator in kubernetes.
    """
    utils.create_ns('strimzi')
    utils.create_ns('kafka')
    utils.add_repo('strimzi', argu.HELM_REPO)
    kafka_op = 'strimzi/strimzi-kafka-operator'
    utils.install_repo('strimzi', 'strimzi', kafka_op, 'kafkaop-strimzi-values.yaml')


@kafkaop.command(name="delete")
def delete():
    """Uninstall strimzi kafka operator from kubernetes.
    """
    utils.uninstall_repo('strimzi', 'strimzi')
    utils.delete_repo('strimzi')
    utils.delete_ns('strimzi')
    

@kafkaop.command(name="create-test-cluster")
@click.argument('kafka_yaml', type=str, required=True)
def create_test_cluster(kafka_yaml: str):
    """Deploy a test kafka cluster using strimzi kafka operator in kubernetes

    Args:
        kafka_yaml (str, required): name of the yaml file where the characteristics of the test cluster are defined.
    """
    utils.run_kubectl_apply(kafka_yaml,'kafka')

@kafkaop.command(name="delete-test-cluster")
@click.argument('kafka_yaml', type=str, required=True)
def delete_test_cluster(kafka_yaml: str):
    """Delete a test kafka cluster using strimzi kafka operator in kubernetes

    Args:
        namespace (str, required): name of the yaml file where the characteristics of the test cluster are defined.
    """
    utils.run_kubectl_delete(resource_yaml=kafka_yaml, namespace='kafka')
    utils.delete_ns('kafka')

@kafkaop.command(name="create-topic")
@click.option('--partitions', '-p', default=1 , help='Number of topic partitions')
@click.option('--replicas', '-r', default=1 , help='Number of topic replicas')
@click.argument('topic_name', type=str, required=True)
def create_topic(topic_name: str, partitions: int, replicas: int):
    """Create a topic in Kafka cluster

    Args:
        topic_name (str, required): topic name to be created.
        partitions (int, optional): number of topic partitions. Defaults to 1.
        replicas (int, optional): number of topic replicas. Defaults to 1.
    """
    data = {
        'apiVersion': 'kafka.strimzi.io/v1beta2',
        'kind': 'KafkaTopic',
        'metadata': {
            'name': topic_name,
            'labels': {
                'strimzi.io/cluster': 'my-cluster'
            }
        },
        'spec': {
            'partitions': partitions,
            'replicas': replicas
        }
    }
    absolute = str(Path(__file__).parent.parent)
    values_path = path.join(absolute, 'resources', 'kafka-topic-create.yaml')
    with open(values_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

    result = utils.run_kubectl_apply(resource_yaml='kafka-topic-create.yaml', namespace='kafka')
    if result.returncode == 0:
        click.echo("-------------------------------------------")
        click.echo(f"Topic {topic_name} created!")
        click.echo("-------------------------------------------")
        
@kafkaop.command(name="delete-topic")
@click.argument('topic_name', type=str, required=True)
def delete_topic(topic_name: str):
    """Delete a topic in Kafka cluster

    Args:
        topic_name (str): Topic name to be created

    Raises:
        SystemError: Error with the stderr from the subprocess
    """
    command = ["kubectl", "delete", "kafkatopic", topic_name, "--namespace", "kafka"]
    result = utils.__run_subprocess(command)
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

@kafkaop.command()
@click.argument('topic_name', type=str, required=True)
@click.option('--message', '-m', default='default message', help='Message to produce')
@click.option('--count', '-c', default=10, type=int, help='Number of messages to produce')
def produce_messages(topic_name: str, message: str, count: int):
    """Create a Kafka producer pod to send messages into a kafka topic

    Args:
        topic_name (str, required): topic to send the messages to
        message (str, optional): message to send. Defaults to 'default message'.
        count (int, required): numbers of message repetitions. Defaults to 10.

    Raises:
        SystemError: Error with the stderr from the subprocess
    """
    command = [
    "kubectl", 
    "-n", "kafka", 
    "run", "kafka-producer",
    "-i",
    "--image=quay.io/strimzi/kafka:0.39.0-kafka-3.6.1", 
    "--restart=Never", 
    "--", 
    "bin/kafka-console-producer.sh", 
    "--bootstrap-server", "my-cluster-kafka-bootstrap:9092", 
    "--topic", topic_name
    ]
    input_messages = "\n".join([f"{message} {i+1}" for i in range(count)]) + "\n"
  
    result = utils.__run_subprocess(command, input=input_messages)
    
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
    
    utils.run_kubectl_delete_with_res("pod", "kafka", "kafka-producer")

@kafkaop.command()
@click.argument('topic_name', type=str, required=True)
@click.option('--latest', '-l', default="true", help='True to consume latest messages. False to consume from beginning')
def consume_messages(topic_name: str, latest: str):
    """Create a Kafka consumer pod to read messages from a kafka topic

    Args:
        topic_name (str, required): topic to read the messages from
        latest (str, optional): set to "true" to consume latest messages. Set to "false" to consume from beginning. Defaults to true.
    """

    if latest == "true":
        command = [
        "kubectl",
        "-n", "kafka",
        "run", "kafka-consumer",
        "-ti",
        "--image=quay.io/strimzi/kafka:0.39.0-kafka-3.6.1",
        "--rm=true",
        "--restart=Never",
        "--",
        "bin/kafka-console-consumer.sh",
        "--bootstrap-server", "my-cluster-kafka-bootstrap:9092",
        "--topic", topic_name
        ]
        click.echo("-------------------------------------------")
        click.echo(f"Printing messages in topic {topic_name}: (Ctrl+c to finish)")
        click.echo("-------------------------------------------")
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Imprimir la salida línea por línea
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
    else:
        command = [
        "kubectl",
        "-n", "kafka",
        "run", "kafka-consumer",
        "-ti",
        "--image=quay.io/strimzi/kafka:0.39.0-kafka-3.6.1",
        "--rm=true",
        "--restart=Never",
        "--",
        "bin/kafka-console-consumer.sh",
        "--bootstrap-server", "my-cluster-kafka-bootstrap:9092",
        "--topic", topic_name,
        "--from-beginning"
        ]
        click.echo("-------------------------------------------")
        click.echo(f"Printing messages from beginning in topic {topic_name}: (Ctrl+c to finish)")
        click.echo("-------------------------------------------")       
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Imprimir la salida línea por línea
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

 


    
@kafkaop.command(name="revision")
def status():
    """Check the revision for this installation
    """
    utils.run_helm_revision('strimzi')
    