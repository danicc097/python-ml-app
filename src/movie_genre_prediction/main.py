import os
from pathlib import Path
from typing import Dict, List, Tuple

from loguru import logger

from src.movie_genre_prediction.model import MovieGenreModel
from src.config.loguru_setup import setup_logger_from_settings


def create_app() -> Tuple[FastAPI, MovieGenreModel]:
    logger.info("Creating movie genre prediction app")

    app = FastAPI()
    setup_logger_from_settings()

    model_manager = MovieGenreModel()

    return app, model_manager


app, model_manager = create_app()


class Title(BaseModel):
    title: str


class MovieGenre(Title):
    predicted_genre: List[str]


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}


@app.post("/predict", response_model=MovieGenre, status_code=status.HTTP_200_OK)
async def get_prediction(payload: Title):
    """
    Predict the damage type of a work item by its title.
    """

    title = payload.title.lower()
    try:
        predictions: List[str] = model_manager.predict(title)
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error while predicting damage type: {e}",
        )

    if not predictions:
        raise HTTPException(status_code=400, detail="Model not found.")

    return MovieGenre(title=title, predicted_genre=predictions)


@app.post("/train", status_code=status.HTTP_200_OK)
async def train_model():
    """
    Train the model with current data in the system.
    """
    try:
        model_manager.train()
        return Response(
            status_code=status.HTTP_200_OK,
            content="movie genre prediction model successfully trained.",
            media_type="text/plain",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e
