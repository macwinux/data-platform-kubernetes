# Redpanda

## Commands

### Install

`dp redpanda install`

Options

- `--version` or `-v`: Redpanda helm chart version
- `--tls` or `-t`: Set TLS configuration in Redpanda
- `--namespace` or `-n`: Namespace where redpanda will be deployed
- `--brokers` or `-b`: How many replica redpanda brokers will be deployed

### Delete

`dp redpanda delete`

Options

- `--namespace` or `-n`: Namespace where redpanda is deployed

### Create Topic

`dp redpanda create_topic test-topic` 

Options

- `--namespace` or `-n` Namespace where redpanda is installed
 
Arguments

- `topic_name` Name of the topic that you want to create.

### Delete Topic

`dp redpanda delete_topic test_topic`

Options

- `--namespace` or `-n` Namespace where redpanda is installed
 
 ### Produce Messages

 `dp redpanda produce_messages test_topic`

 Options

 - `--namespace` or `-n` Namespace where redpanda is installed
 - `--message` or `-m` Message to produce
 - `--count` or `-c` Number of messages to produce

 