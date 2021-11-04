from io import BytesIO
from pathlib import Path

import torch
import numpy as np
from PIL import Image
from torchvision.transforms import transforms

from app.core.nvae import utils
from app.core.nvae.model import AutoEncoder

MODEL_PATH: Path = Path(Path(__file__).resolve().parent, 'duke_model.pt')

checkpoint = torch.load(MODEL_PATH, map_location=torch.device('cpu'))
args = checkpoint['args']
args.batch_size = 1
model = AutoEncoder(args, None, utils.get_arch_cells(args.arch_instance))
model.load_state_dict(checkpoint['state_dict'], strict=False)
model = model.cpu()
model = model.eval()


def transform_image(image_bytes):
    my_transforms = transforms.Compose([transforms.Resize((32, 32)),
                                        transforms.ToTensor()])
    image = Image.open(BytesIO(image_bytes))
    image = image.convert('RGB')
    return my_transforms(image).unsqueeze(0)


def predict(img_bytes1, img_bytes2):
    # tensor1 = transform_image(image_bytes=img_bytes1)
    # tensor2 = transform_image(image_bytes=img_bytes2)
    # tensor = (tensor1 + tensor2) / 2
    # logits, log_q, log_p, kl_all, kl_diag = model(tensor)
    n = int(np.floor(np.sqrt(1)))
    logits = model.sample(n, 1)
    output = model.decoder_output(logits)
    output_img = output.mean if isinstance(output, torch.distributions.bernoulli.Bernoulli) \
        else output.sample()
    output_tiled = utils.tile_image(output_img, n).detach().numpy().transpose(1, 2, 0)
    output_tiled = np.asarray(output_tiled * 255, dtype=np.uint8)
    output_tiled = np.squeeze(output_tiled)
    img = Image.fromarray(output_tiled)

    return img


def decode(logits, temperature):
    n = int(np.floor(np.sqrt(1)))
    output = model.decoder_output(logits)
    output_img = output.mean if isinstance(output, torch.distributions.bernoulli.Bernoulli) \
        else output.sample(t=temperature)
    output_tiled = utils.tile_image(output_img, n).detach().numpy().transpose(1, 2, 0)
    output_tiled = np.asarray(output_tiled * 255, dtype=np.uint8)
    output_tiled = np.squeeze(output_tiled)
    img = Image.fromarray(output_tiled)

    return img
