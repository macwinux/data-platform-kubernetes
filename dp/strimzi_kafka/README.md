# Kafka Strimzi Operator

## Commands

### Install

`dp kafkaop install`

### Delete

`dp kafkaop delete`

### Deploy a test kafka cluster ([kafka-ephemeral.yaml ](https://github.com/strimzi/strimzi-kafka-operator/blob/main/examples/kafka/kafka-ephemeral.yaml))

`dp kafkaop create-test-cluster kafka-ephemeral.yaml`

### Delete the test kafka cluster

`dp kafkaop delete-test-cluster kafka-ephemeral.yaml`

### Create topic

`dp kafkaop create-topic prueba1`

### Delete topics

`dp kafkaop delete-topic prueba1`

### Get topics

`dp kafkaop get-topics`

### Produce messages

`dp kafkaop produce-messages prueba1 -m "mensaje de prueba" -c 5`

Options

- `--messages` or `-m`: Text of the message to be sent.
- `--count` or `-c`: Number of message repetitions.

### Consume messages

`dp kafkaop consume-messages prueba1 -- latest true`

Options

- `--latest` or `-l`: Consume messages from the beginning of the topic.