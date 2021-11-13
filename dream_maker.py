import torch
import torch.nn as nn
from torch.autograd import Variable
from torchvision import transforms
import torchvision.models as models
import PIL.Image as Image
from tqdm import tqdm
import os

import matplotlib.pyplot as plt


class DreamMaker():
    def __init__(self):
        self.current_dir = os.path.dirname(__file__)
        model_dir = os.path.join(self.current_dir, 'models')
        self.device = torch.device(
            'cuda:0' if torch.cuda.is_available() else 'cpu')
        self.model = models.vgg19_bn(progress=False)
        self.model.load_state_dict(torch.load(
            os.path.join(model_dir, 'vgg19_bn')))
        print(self.model.eval())
        

        print(f'utilizing {self.device}')

    def dream(self, image, size=256, nLayer=0, nSubLayer=41,
              lr=0.001, iterations=40, nOct=2, octZoom=2):

        x = self.toTensor(image, size)
        dream = self.process(x, nLayer, nSubLayer,
                             lr, iterations, nOct, octZoom)

        return self.toPNG(dream)

    def process(self, x, nLayer, nSubLayer,
                lr, iterations, nOct, octZoom):
        layers = list(self.model.children())[:nLayer]
        sub_layers = list(list(self.model.children())[
                          nLayer].children())[:nSubLayer]
        
        dream_model = nn.Sequential(*(layers + sub_layers)).to(self.device)
        x = x.to(self.device)

        octaves = [x]
        oct = x[:]
        for _ in range(nOct - 1):
            oct = self.zoom(oct, octZoom)
            octaves.append(oct)

        

        detail = torch.zeros_like(octaves[-1])
        for oct, oct_base in enumerate(octaves[::-1]):
            print(oct_base.shape)
            if oct > 0:
                detail = self.unZoom(detail, oct_base.shape[2:])

            in_x = oct_base + detail
            dream_x = self.dreamGen(in_x, dream_model, lr, iterations)
            detail = dream_x - oct_base

        return dream_x

    def dreamGen(self, x, model, lr, iterations):
        x = Variable(x, requires_grad=True)
        #blur = transforms.GaussianBlur(5, 0.1)
        for _ in tqdm(range(iterations)):
            model.zero_grad()
            out = model(x)
            loss = out.norm()
            loss.backward()
            #g = blur(x.grad)
            g = x.grad
            avr_grad = torch.abs(x.grad.data).mean()
            norm_lr = lr / avr_grad
            x.data += g[:] * norm_lr
            x.data = self.clip(x.data)
            x.grad.data.zero_()

        return x.data



    @staticmethod
    def clip(x):
        x = x * (x < 1) + (x > 1)
        x = x * (x > 0)
        return x

    @staticmethod
    def zoom(x, zoom_n):
        transform = transforms.Resize(int(x.shape[-1] / zoom_n))
        return transform(x)

    @staticmethod
    def unZoom(x, shape):
        return transforms.Resize(shape)(x)

    @staticmethod
    def toTensor(image, size):
        trans = transforms.Compose([
            transforms.Resize(size),
            transforms.CenterCrop(size),
            transforms.ToTensor()
        ])
        return trans(image)[:3].unsqueeze(0)

    @staticmethod
    def toPNG(tensor):
        return transforms.ToPILImage()(tensor[0])

