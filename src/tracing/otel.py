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
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.propagate import set_global_textmap
from opentelemetry.baggage.propagation import W3CBaggagePropagator
from opentelemetry.propagators.composite import CompositePropagator
from opentelemetry.propagators.jaeger import JaegerPropagator


def configure_tracing():
    resource = Resource(attributes={SERVICE_NAME: "python-ml-grpc-server"})

    # https://www.jaegertracing.io/docs/1.23/apis/#thrift-over-http-stable
    jaeger_exporter = JaegerExporter(
        collector_endpoint="http://localhost:14268/api/traces"
    )

    set_global_textmap(
        # CompositePropagator([TraceContextTextMapPropagator(), W3CBaggagePropagator()])
        # best way to propagate between services is to use the specific jaeger propagator.
        # alternatively Jaeger supports Zipkin B3 format and W3C Trace-Context (requires further setup)
        # https://www.jaegertracing.io/docs/1.19/client-libraries/#propagation-format
        JaegerPropagator()
    )

    provider = TracerProvider(resource=resource)
    provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))
    # traces logged to stdout
    provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(provider)

    GrpcInstrumentorClient().instrument()

    GrpcInstrumentorServer().instrument()
