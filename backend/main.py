import time

from typing import Optional
from fastapi import FastAPI, Header
from fastapi.responses import ORJSONResponse, RedirectResponse, PlainTextResponse

from fastapi import FastAPI
from argparse import Namespace
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from utils import deps1


def get_application() -> FastAPI:
    trace.set_tracer_provider(TracerProvider())
    jaeger_exporter = JaegerExporter(
        agent_host_name="jaeger",
        agent_port=6831,
    )
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(jaeger_exporter, max_export_batch_size=10)
    )

    application = FastAPI(
        title="Jaeger with FastAPI",
        version="1.0",
        description="Do something awesome, while being monitored.",
        default_response_class=ORJSONResponse,
    )

    FastAPIInstrumentor.instrument_app(application)
    return application


app = get_application()
tracer = trace.get_tracer(__name__)


@app.get("/", status_code=200)
async def docs() -> RedirectResponse:
    return RedirectResponse(url="/docs")


@app.get("/span", status_code=200)
async def get_status(task_id: Optional[str] = Header(None)) -> PlainTextResponse:
    with tracer.start_as_current_span(
        "parent", attributes={"task_id": task_id}
    ) as parent:
        parent.add_event("parent's event")
        time.sleep(0.5)
        with tracer.start_as_current_span("child") as child:
            child.add_event("child's event")
            deps1()
    return PlainTextResponse(content="\n")
