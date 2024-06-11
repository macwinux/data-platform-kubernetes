## Setup Requirements

1.  If you don't have the venv environmnet created:
`python3 -m venv .venv`
2.  Then, activate it (if you're using Windows, you need to have administrator perms):
`.venv\Scripts\activate`
3.  `pip install -r requirements.txt`
4. Now, you can run for example, flink operator with:
`dp.py flinkop install` or `dp.py flinkop install 1.8.0`
or you can run redpanda heml chart with:
`dp.py flink install -n redpanda`

#### Run test
`python -m unittest`

#### Create the binary 

`pyinstaller -F --paths=dp --add-data="dp/resources:resources" .\dp\dp.py`
The binary will be in dist folder.

[Flink Operator](dp/flinkop/README.md)

[Redpanda](dp/redpanda_helm/README.md)

[ScyllaDB](dp/scylladb/README.md)

[Sparkop](dp/sparkop/README.md)

[Miniop](dp/miniop/README.md)

[Kafkaop](dp/strimzi_kafka/README.md)