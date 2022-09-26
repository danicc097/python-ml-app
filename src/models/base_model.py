import os
from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import Any, Optional, Type, TypeVar, cast

import joblib


class MLBaseModel(metaclass=ABCMeta):
    def __init__(self, *args, **kwargs):
        pass

    def validate_path(self, path: str):
        """
        Ensures a ``.joblib`` path is passed.
        """
        if Path(path).suffix != ".joblib":
            raise ValueError("The model path must be a valid ``.joblib`` file.")

    def save_model(self, model, path: str):
        """
        Save the model to a ``.joblib`` file.
        """
        # scikit-learn recommends using joblib for saving models
        joblib.dump(model, path)

    def load_model(self, path: str) -> Optional[Any]:
        """
        Load the model from a ``.joblib`` file.
        """
        self.validate_path(path)
        if not os.path.exists(path):
            print(f"\n\nModel file {path} does not exist.\n\n")
            return None

        return joblib.load(path)

    @abstractmethod
    def train(self) -> Any:
        pass

    @abstractmethod
    def predict(self, X: Any):
        pass
