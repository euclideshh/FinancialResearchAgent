import base64
import os
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk import trace as trace_sdk
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry import trace
from dotenv import load_dotenv

def init_tracing():
    load_dotenv()
    # Configure Weave endpoint and authentication
    WANDB_BASE_URL = os.getenv("WANDB_BASE_URL", "https://trace.wandb.ai")  
    PROJECT_ID = os.getenv("WANDB_PROJECT")
    OTEL_EXPORTER_OTLP_ENDPOINT = f"{WANDB_BASE_URL}/otel/v1/traces"

    # Set up authentication
    WANDB_API_KEY = os.getenv("WANDB_API_KEY")
    os.environ["WANDB_API_KEY"] = WANDB_API_KEY
    AUTH = base64.b64encode(f"api:{WANDB_API_KEY}".encode()).decode()

    OTEL_EXPORTER_OTLP_HEADERS = {
        "Authorization": f"Basic {AUTH}",
        "project_id": PROJECT_ID,
    }

    # Create the OTLP span exporter with endpoint and headers
    exporter = OTLPSpanExporter(
        endpoint=OTEL_EXPORTER_OTLP_ENDPOINT,
        headers=OTEL_EXPORTER_OTLP_HEADERS,
    )

    # Create a tracer provider and add the exporter
    tracer_provider = trace_sdk.TracerProvider()
    tracer_provider.add_span_processor(SimpleSpanProcessor(exporter))

    # Set the global tracer provider BEFORE importing/using ADK
    trace.set_tracer_provider(tracer_provider)

    #####print("Tracing initialized with Weave endpoint:", OTEL_EXPORTER_OTLP_ENDPOINT)
