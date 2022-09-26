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
                usecols=["title", "genres"],
                converters={"genres": lambda x: x.split("|")},
            )
        except Exception as e:
            logger.error(e)
            raise Exception(f"Invalid csv data in {csv_path} for MovieGenreModel")
        self.df = self.df.explode("genres")
        self.df.dropna(inplace=True)
        self.df.drop_duplicates(inplace=True)
        self.corpus = self.df["title"].tolist()

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
            stop_words=None,
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

        input_title = X.lower()
        input_title = self.vectorizer.transform([input_title])

        pairwise_similarity = cosine_similarity_n_space(self.tfidf_matrix, input_title)

        top_indeces = np.argsort(pairwise_similarity, axis=0)[-10:]
        top_indeces = reversed(top_indeces)
        top_indeces = [i[0] for i in top_indeces]

        for _, title_idx in enumerate(top_indeces):
            logger.debug(
                f"{self.corpus[title_idx]} ::: {pairwise_similarity[title_idx][0]}"
            )
        predictions = self.df.iloc[top_indeces]["genres"].tolist()
        logger.info(predictions)

        return predictions
