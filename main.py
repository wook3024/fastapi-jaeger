import time
import yaml

from fastapi import FastAPI
from omegaconf import OmegaConf
from jaeger_client import Config
from fastapi.responses import ORJSONResponse


with open("tracing-config.yaml", encoding="utf8") as f:
    yaml_dict = yaml.safe_load(f)
conf = OmegaConf.create(yaml_dict)
config = Config(config=conf.get("config"))
tracer = config.initialize_tracer()


app = FastAPI(
    title="Jaeger with FastAPI",
    default_response_class=ORJSONResponse,
)


@app.get("/span/{id}", status_code=200)
def get_status(id: str) -> ORJSONResponse:
    with tracer.start_span("ParentSpan") as span:
        span.log_kv({"event": "test message", "life": 42})
        time.sleep(2)
        with tracer.start_span("ChildSpan", child_of=span) as child_span:
            child_span.log_kv({"event": "down below"})
    return ORJSONResponse(content="\n")
