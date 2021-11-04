import os

import torch

DAO_FOLDER: str = os.path.dirname(os.path.realpath(__file__))


class ModelDB:

    @staticmethod
    def get_or_404(model_name, dataset_name, size):
        model_path = os.path.join(
            DAO_FOLDER, 'models', model_name, dataset_name, size, 'model.pt')
        return torch.load(model_path)
