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