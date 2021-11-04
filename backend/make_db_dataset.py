from pathlib import Path

import numpy as np
import torch
import umap
from PIL import Image, ImageOps

from torchvision.transforms import transforms

from app.core.nvae import utils
from app.core.nvae.model import AutoEncoder

DUKE_PNG_DIR = Path('/home/gabriel/Documents/embedding_combiner/frontend/duke/')
MODEL_PATH = '/home/gabriel/Documents/embedding_combiner/backend/app/core/model.pt'


def main():
    checkpoint = torch.load(MODEL_PATH, map_location=torch.device('cpu'))
    args = checkpoint['args']
    args.batch_size = 1
    model = AutoEncoder(args, None, utils.get_arch_cells(args.arch_instance))
    model.load_state_dict(checkpoint['state_dict'], strict=False)
    model = model.cpu()
    model = model.eval()
    my_transforms = transforms.Compose([transforms.Resize((32, 32)),
                                        transforms.ToTensor()])
    arr_imgs = []
    tensor_imgs = []
    labels = []
    img_names = []
    file_ending = '*.png'
    oct_paths = list(DUKE_PNG_DIR.glob(file_ending))
    for oct_path in oct_paths:
        with Image.open(oct_path) as pil_img:
            img_name = str(oct_path).split('/')[-1]
            img_names.append(img_name)
            labels.append(img_name.split('_')[0])
            gray_image = ImageOps.grayscale(pil_img)
            arr_imgs.append(np.array(gray_image).flatten())
            tensor_imgs.append(my_transforms(pil_img))
    mat_imgs = np.stack(arr_imgs) / 255.
    projection = umap.UMAP().fit_transform(mat_imgs)
    embedding, _, _, _, _ = model(torch.stack(tensor_imgs))
    embedding = embedding.detach().numpy()
    np.savez('raw_data/duke_db_dataset.npz',
             labels=labels,
             img_names=img_names,
             x=projection[:, 0],
             y=projection[:, 1],
             embedding=embedding)


if __name__ == '__main__':
    main()
