import random
from pathlib import Path

import numpy as np
import torch
import umap
from PIL import Image

from torch.utils.data import Subset
from torchvision.transforms import transforms
from tqdm import tqdm

from app.core.nvae import utils
from app.core.nvae.lmdb_datasets import LMDBDataset
from app.core.nvae.model import AutoEncoder

LMDB_DIR = Path('/home/gabriel/Documents/embedding_combiner/frontend/images/celeba/celeba-lmdb')
PNG_DIR = Path('/home/gabriel/Documents/embedding_combiner/frontend/images/celeba/celeba-png')
MODEL_PATH = '/home/gabriel/Documents/embedding_combiner/backend/app/core/celeba_model.pt'


def main():
    torch.manual_seed(42)
    np.random.seed(42)
    random.seed(42)
    checkpoint = torch.load(MODEL_PATH, map_location=torch.device('cpu'))
    args = checkpoint['args']
    # args.num_channels_enc = 30
    # args.num_channels_dec = 30
    # args.num_postprocess_cells = 2
    # args.num_preprocess_cells = 2
    # args.num_latent_scales = 5
    # args.num_latent_per_group = 20
    # args.num_cell_per_cond_enc = 2
    # args.num_cell_per_cond_dec = 2
    # args.num_preprocess_blocks = 1
    # args.num_postprocess_blocks = 1
    # args.num_groups_per_scale = 16
    # args.min_groups_per_scale = 4
    # args.num_process_per_node = 8
    # args.ada_groups = True

    model = AutoEncoder(args, None, utils.get_arch_cells(args.arch_instance))
    model.load_state_dict(checkpoint['state_dict'], strict=False)
    model = model.cpu()
    model = model.eval()
    my_transforms = transforms.Compose([transforms.ToTensor()])
    arr_imgs = []
    train_data = Subset(LMDBDataset(root=LMDB_DIR, name='celeba', train=True), range(500))
    for index, img_and_label in enumerate(tqdm(train_data)):
        img, label = img_and_label
        arr_img = np.array(img)
        img = img.resize((64, 64))
        img.save(Path(PNG_DIR, "img_{}.png".format(index)))
        arr_imgs.append(arr_img.flatten())
    arr_imgs = np.stack(arr_imgs) / 255.
    projection = umap.UMAP(low_memory=True).fit_transform(arr_imgs)
    del arr_imgs
    imgs = []
    img_names = []
    labels = []
    for index, img_and_label in enumerate(tqdm(train_data)):
        img, label = img_and_label
        img = img.resize((64, 64))
        img_name = 'img_{}.png'.format(index)
        img_names.append(img_name)
        labels.append(label)
        embedding, _, _, _, _ = model(torch.unsqueeze(my_transforms(img), 0))
        imgs.append(embedding.detach().numpy())
    imgs = np.concatenate(imgs, axis=0)
    np.savez('raw_data/celeba_db_dataset_embeddings.npz',
             labels=labels,
             img_names=img_names,
             x=projection[:, 0],
             y=projection[:, 1],
             embedding=imgs)


if __name__ == '__main__':
    main()
