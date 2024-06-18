import click
import utils.subprocess_com as utils
import utils.helm_const as h
import utils.constants as c
from os import path
from pathlib import Path
import yaml

@click.group()
def kafkaop():
    """
        Install strimzi kafka operator command.
    """

@kafkaop.command(name='install')
def install():
    """Install strimzi kafka operator in kubernetes.
    """
    utils.create_ns(c.KAFKA_NS_OP)
    utils.create_ns(c.KAFKA_NS)
    utils.add_repo(c.KAFKA_REPO, h.HELM_KAFKA_REPO)
    utils.install_repo(c.KAFKA_NS_OP, c.KAFKA_REPO, c.KAFKA_OP, c.KAFKA_OP_VALUES)


@kafkaop.command(name="delete")
def delete():
    """Uninstall strimzi kafka operator from kubernetes.
    """
    utils.uninstall_repo(c.KAFKA_NS_OP, c.KAFKA_REPO)
    utils.delete_repo(c.KAFKA_REPO)
    utils.delete_ns(c.KAFKA_NS_OP)
    

@kafkaop.command(name="create-test-cluster")
@click.argument('kafka_yaml', type=str, required=True)
def create_test_cluster(kafka_yaml: str):
    """Deploy a test kafka cluster using strimzi kafka operator in kubernetes

    Args:
        kafka_yaml (str, required): name of the yaml file where the characteristics of the test cluster are defined.
    """
    utils.run_kubectl_apply(kafka_yaml,c.KAFKA_NS)

@kafkaop.command(name="delete-test-cluster")
@click.argument('kafka_yaml', type=str, required=True)
def delete_test_cluster(kafka_yaml: str):
    """Delete a test kafka cluster using strimzi kafka operator in kubernetes

    Args:
        kafka_yaml (str, required): name of the yaml file where the characteristics of the test cluster are defined.
    """
    #This block of code delete all the topics running in the cluster. This is nededeed to avoid having kafka namescpace "Terminating"without finishing
    list_command_return = ["kubectl", "get", "kafkatopic", "-n", c.KAFKA_NS, "-o", "jsonpath={.items[*].metadata.name}"]
    result_return = utils.__run_subprocess(list_command_return)
    topics = result_return.stdout.decode('utf-8').split()
    if topics:
        for topic in topics:
            delete_topic_name(topic)  

    utils.run_kubectl_delete(resource_yaml=kafka_yaml, namespace=c.KAFKA_NS)
    utils.delete_ns(c.KAFKA_NS)

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
    values_path = path.join(absolute, 'resources', c.KAFKA_VALUES)
    with open(values_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

    result = utils.run_kubectl_apply(resource_yaml=c.KAFKA_VALUES, namespace=c.KAFKA_NS)
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
    delete_topic_name(topic_name)

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
    "-n", c.KAFKA_NS, 
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
    
    utils.run_kubectl_delete_with_res("pod", c.KAFKA_NS, "kafka-producer")

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
        "-n", c.KAFKA_NS,
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
        utils.__run_Popen(command, text=True)
    else:
        command = [
        "kubectl",
        "-n", c.KAFKA_NS,
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
        utils.__run_Popen(command, text=True)

   
@kafkaop.command(name="revision")
def status():
    """Check the revision for this installation
    """
    utils.run_helm_revision(c.KAFKA_NS_OP)

@kafkaop.command(name="get-topics")
def get_topics():
    """Get all the topics running in the cluster
    """
    list_command = ["kubectl", "get", "kafkatopic", "-n", c.KAFKA_NS]
    result = utils.__run_subprocess(list_command)
    click.echo("-------------------------------------------")
    click.echo(f"{result.stdout.decode('utf-8')}")
    click.echo("-------------------------------------------")

def delete_topic_name(topic_name: str):
    command = ["kubectl", "delete", "kafkatopic", topic_name, "--namespace", c.KAFKA_NS]
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