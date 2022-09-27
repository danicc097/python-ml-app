from asyncio import futures
import os
from pathlib import Path
import time
from typing import Dict, List, Tuple

from loguru import logger

from src.movie_genre_prediction.model import MovieGenreModel
from src.config.loguru_setup import setup_logger_from_settings
from src.pb.tfidf.v1.service_pb2 import *
import src.pb.tfidf.v1.service_pb2_grpc as tfidf_grpc


class MovieGenreService(tfidf_grpc.MovieGenreServicer):
    def GetGenre():
        pass


logger.info("Creating movie genre prediction app")
setup_logger_from_settings()
server = tfidf_grpc.grpc.server(futures.ThreadPoolExecutor(max_workers=10))
tfidf_grpc.add_MovieGenreServicer_to_server(MovieGenreService(), server)
server.add_insecure_port("[::]:" + str(8900))
server.start()
print("Listening on port {}..".format(8900))
try:
    while True:
        time.sleep(10000)
except KeyboardInterrupt:
    server.stop(0)
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
