import logging
from fastapi import FastAPI, HTTPException
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource

# Configuração do OpenTelemetry
resource = Resource(attributes={
    "service.name": "fastapi-app",
    "deployment.environment": "development"
})

trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

# Configuração do exportador OTLP
otlp_exporter = OTLPSpanExporter(endpoint="http://otel-collector:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Configuração do logging
LoggingInstrumentor().instrument()
logger = logging.getLogger(__name__)

app = FastAPI()
FastAPIInstrumentor.instrument_app(app)

@app.get("/")
async def root():
    logger.info("Acessando endpoint raiz")
    return {"message": "Bem-vindo à API de Observabilidade"}

@app.get("/health")
async def health_check():
    logger.info("Verificando saúde da aplicação")
    return {"status": "healthy"}

@app.get("/error")
async def generate_error():
    logger.error("Gerando erro intencional")
    raise HTTPException(status_code=500, detail="Erro intencional gerado")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 