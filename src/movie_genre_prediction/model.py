import os
from pathlib import Path
from re import S
from typing import Any, Optional, Tuple

import joblib
import numpy as np
import pandas as pd
from loguru import logger
from sklearn.feature_extraction.text import TfidfVectorizer

from src.config.config import DATA_DIR
from src.models.base_model import MLBaseModel
from src.utils.metrics import cosine_similarity_n_space
from src.utils.timing import func_timer

CWD = Path(os.path.dirname(os.path.abspath(__file__)))


class MovieGenreModel(MLBaseModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._initialized = False

    def _get_data(self):
        csv_path = DATA_DIR / "movies.csv"
        try:
            self.df = pd.read_csv(
                csv_path,
                delimiter=",",
                usecols=["plot_synopsis", "tags"],
                converters={"tags": lambda x: x.split(", ")},
            )
        except Exception as e:
            raise Exception(f"Invalid csv data in {csv_path} for MovieGenreModel: {e}")
        self.df = self.df.explode("tags")
        self.df.dropna(inplace=True)
        self.df.drop_duplicates(inplace=True)
        self.corpus = self.df["plot_synopsis"].tolist()

    @func_timer
    def _vectorize_corpus(self):
        self.tfidf_matrix = self.vectorizer.transform(self.corpus)

    @func_timer
    def train(self, *args, **kwargs):
        self._get_data()
        tfidf_vect = TfidfVectorizer(
            max_features=500,
            lowercase=True,
            ngram_range=(1, 1),
            stop_words="english",
            max_df=0.5,
            min_df=2,
            norm="l2",
        )
        self.vectorizer = tfidf_vect.fit(self.corpus)
        self._vectorize_corpus()

        self.save_model(self.vectorizer, CWD / "vectorizer.joblib")

        return self.vectorizer

    def predict(self, X: str):
        if not self._initialized:
            self._get_data()
            self.vectorizer = self.load_model(str(CWD / "vectorizer.joblib"))
            if not self.vectorizer:
                self.vectorizer = self.train()
            else:
                self._vectorize_corpus()
            self._initialized = True
            logger.info("MovieGenreModel initialized")

        input_synopsis = X.lower()
        input_synopsis = self.vectorizer.transform([input_synopsis])

        pairwise_similarity = cosine_similarity_n_space(
            self.tfidf_matrix, input_synopsis
        )

        top_indeces = np.argsort(pairwise_similarity, axis=0)[-10:]
        top_indeces = reversed(top_indeces)
        top_indeces = [i[0] for i in top_indeces]

        predictions = self.df.iloc[top_indeces]["tags"].tolist()
        logger.info(predictions)

        return predictions


m = MovieGenreModel()
m.predict(
    """
When their kingdom becomes trapped in perpetual winter, fearless Anna (Kristen Bell) joins forces with mountaineer Kristoff (Jonathan Groff) and his reindeer sidekick to find Anna's sister, Snow Queen Elsa (Idina Menzel), and break her icy spell. Although their epic journey leads them to encounters with mystical trolls, a comedic snowman (Josh Gad), harsh conditions, and magic at every turn, Anna and Kristoff bravely push onward in a race to save their kingdom from winter's cold grip.
"""
)
