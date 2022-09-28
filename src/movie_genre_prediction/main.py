from concurrent import futures
import os
from pathlib import Path
import time
from typing import Dict, List, Tuple

from loguru import logger

from src.movie_genre_prediction.model import MovieGenreModel
from src.config.loguru_setup import setup_logger_from_settings
from src.pb.tfidf.v1 import service_pb2
from src.pb.tfidf.v1 import service_pb2_grpc
import grpc
from src.tracing.otel import configure_tracing
from opentelemetry import baggage, trace

tracer = trace.get_tracer(__name__)


class MovieGenreService(service_pb2_grpc.MovieGenreServicer):
    def __init__(self) -> None:
        super().__init__()
        logger.info("Creating movie genre prediction service")
        self.model_manager = MovieGenreModel()
        self.model_manager.initialize()

    def Predict(self, request: service_pb2.PredictRequest, context):
        predictions = self.model_manager.predict(request.synopsis)

        with tracer.start_span(name="MovieGenreService.Predict") as span:
            ctx = baggage.set_baggage("foo", "bar")
            logger.debug(f"Global context baggage: {baggage.get_all()}")
            logger.debug(f"Span context baggage: {baggage.get_all(context=ctx)}")
            return service_pb2.PredictReply(
                predictions=[service_pb2.Prediction(genre=p) for p in predictions]
            )

    def Train(self, request: service_pb2.TrainRequest, context):
        self.model_manager.train()

        return service_pb2.TrainReply(
            message="Successfully trained movie genre prediction model"
        )


setup_logger_from_settings()
configure_tracing()

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))


movie_genre_service = MovieGenreService()
service_pb2_grpc.add_MovieGenreServicer_to_server(movie_genre_service, server)
port = 50051
server.add_insecure_port(f"[::]:{port}")
server.start()
logger.info(f"Listening on port {port}...")
server.wait_for_termination()

# m = MovieGenreModel()
# m.predict(
#     """
# When their kingdom becomes trapped in perpetual winter, fearless Anna (Kristen Bell) joins forces with mountaineer Kristoff (Jonathan Groff) and his reindeer sidekick to find Anna's sister, Snow Queen Elsa (Idina Menzel), and break her icy spell. Although their epic journey leads them to encounters with mystical trolls, a comedic snowman (Josh Gad), harsh conditions, and magic at every turn, Anna and Kristoff bravely push onward in a race to save their kingdom from winter's cold grip.
# """
# )


# def create_app() -> Tuple[FastAPI, MovieGenreModel]:
#
#     app = FastAPI()
#

#     model_manager = MovieGenreModel()

#     return app, model_manager


# app, model_manager = create_app()


# class Title(BaseModel):
#     title: str


# class MovieGenre(Title):
#     predicted_genre: List[str]


# @app.get("/ping")
# async def pong():
#     return {"ping": "pong!"}


# @app.post("/predict", response_model=MovieGenre, status_code=status.HTTP_200_OK)
# async def get_prediction(payload: Title):
#     """
#     Predict the damage type of a work item by its title.
#     """

#     title = payload.title.lower()
#     try:
#         predictions: List[str] = model_manager.predict(title)
#     except Exception as e:
#         logger.error(e)
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Error while predicting damage type: {e}",
#         )

#     if not predictions:
#         raise HTTPException(status_code=400, detail="Model not found.")

#     return MovieGenre(title=title, predicted_genre=predictions)


# @app.post("/train", status_code=status.HTTP_200_OK)
# async def train_model():
#     """
#     Train the model with current data in the system.
#     """
#     try:
#         model_manager.train()
#         return Response(
#             status_code=status.HTTP_200_OK,
#             content="movie genre prediction model successfully trained.",
#             media_type="text/plain",
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
#         ) from e
