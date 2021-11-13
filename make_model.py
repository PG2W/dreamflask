import torch
import torchvision.models as models
import os

model = models.vgg19_bn(pretrained=True)

current_dir = os.path.dirname(__file__)
models_dir = os.path.join(current_dir, 'models')

torch.save(model.state_dict(), os.path.join(models_dir, 'vgg19_bn'))

