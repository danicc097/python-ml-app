from opentelemetry import trace

# from opentelemetry.exporter.jaeger.proto.grpc import JaegerExporter

from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, BatchSpanProcessor
from opentelemetry.instrumentation.grpc import (
    GrpcInstrumentorClient,
    GrpcInstrumentorServer,
)


def configure_tracing():
    resource = Resource(attributes={SERVICE_NAME: "python-ml-grpc-server"})

    # https://www.jaegertracing.io/docs/1.23/apis/#thrift-over-http-stable
    jaeger_exporter = JaegerExporter(
        collector_endpoint="http://localhost:14268/api/traces"
    )

    provider = TracerProvider(resource=resource)
    provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))
    # traces logged to stdout
    provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(provider)

    GrpcInstrumentorClient().instrument()

    GrpcInstrumentorServer().instrument()
