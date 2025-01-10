## Setup Requirements

1.  If you don't have the uv installed, follow uv documentation:
[uv](https://github.com/astral-sh/uv?tab=readme-ov-file#python-management)
2. `uv sync --all-extras --dev`
3. Now, you can run for example, flink operator with:
`uv run dp.py flinkop install` or `uv run dp.py flinkop install 1.8.0`
or you can run redpanda heml chart with:
`uv run dp.py flink install -n redpanda`

#### Run test
`uv run pytest`

#### Create the binary 
You need to install pyinstaller in your local or in the venv with `pip install pyinstaller`:
`uv tool install pyinstaller`
`uv run pyinstaller -F --paths=dp --add-data="dp/resources:resources" .\dp\dp.py`

The binary will be in dist folder.

[Flink Operator](dp/flinkop/README.md)

[Redpanda](dp/redpanda_helm/README.md)

[ScyllaDB](dp/scylladb/README.md)

[Sparkop](dp/sparkop/README.md)

[Miniop](dp/miniop/README.md)

[Kafkaop](dp/strimzi_kafka/README.md)