from pydoc import locate
import pandas as pd


class Dataset:

    @staticmethod
    def load(dataset, **params) -> pd.DataFrame:

        tokenize = dataset.title().replace('_', '')

        dataset_class = locate(f'sns_flow.model.datasets.{tokenize}.{tokenize}')

        if dataset_class is None:
            raise NameError(f'Class with name "datasets.{tokenize}"" not found!')

        return dataset_class(**params)



