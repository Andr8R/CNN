"""
GeneratorDiscrimantor.py

PyTorch implementation of Generator and Disciminator models for GAN using ResNet-style architecture.

End caps 'pasted' into data.
"""
# For debugging
import pdb

# PyTorch imports
from torch.nn import Module, Sequential, Linear, Conv2d, ConvTranspose2d, BatchNorm2d, ReLU, LeakyReLU, Sigmoid, Tanh
from torch.nn.init import kaiming_normal_, constant_

# WatChMaL imports
from models import resnetblocks

# Global variables
__all__ = ['genresnet18', 'genresnet34', 'genresnet50', 'genresnet101', 'genresnet152',
           'disresnet18', 'disresnet34', 'disresnet50', 'disresnet101', 'disresnet152']
_RELU = ReLU()
_LeakyRELU = LeakyReLU(0.2, True)
_Sigmoid = Sigmoid()
_Tanh = Tanh()

# -------------------------------
# Generator architecture layers
# -------------------------------

class Generator(Module):

    def __init__(self, block1, block2, layers, num_input_channels, num_latent_dims, zero_init_residual=False):
        
        super().__init__()
        
        ngf = 64
        nc = num_input_channels
        self.conv1 = ConvTranspose2d(num_latent_dims, ngf * 8, 4, 2, 0, bias=False)
        self.bn1 = BatchNorm2d(ngf * 8)
        
        self.conv2 = ConvTranspose2d(ngf * 8, ngf * 4, 3, 3, 1, bias=False)
        self.bn2 = BatchNorm2d(ngf * 4)
        
        self.conv3 = ConvTranspose2d( ngf * 4, ngf * 2, 4, 2, 1, bias=False)
        self.bn3 = BatchNorm2d(ngf * 2)
        
        self.conv4 = ConvTranspose2d( ngf * 2, ngf, 4, 2, 1, bias=False)
        self.bn4 = BatchNorm2d(ngf)
        
        self.conv5 = ConvTranspose2d( ngf, nc, 3, 1, 1, bias=False)

    def forward(self, X):        
        x = self.conv1(X)
        x = self.bn1(x)
        x = _RELU(x)
       
        x = self.conv2(x)
        x = self.bn2(x)
        x = _RELU(x)
       
        x = self.conv3(x)
        x = self.bn3(x)
        x = _RELU(x)
     
        x = self.conv4(x)
        x = self.bn4(x)
        x = _RELU(x)

        x = self.conv5(x)
        
        return x

#-------------------------------
# Discriminator architecture layers
#-------------------------------
class Discriminator(Module):

    def __init__(self, block1, block2, layers, num_input_channels, num_latent_dims, zero_init_residual=False):
        
        super().__init__()
        
        nc = num_input_channels
        ndf = 64
        
        self.main = Sequential(
            # input is (nc) x 64 x 64
            Conv2d(nc, ndf, 4, 2, 1, bias=False),
            LeakyReLU(0.2, inplace=True),
            # state size. (ndf) x 32 x 32
            Conv2d(ndf, ndf * 2, 4, 2, 1, bias=False),
            BatchNorm2d(ndf * 2),
            LeakyReLU(0.2, inplace=True),
            # state size. (ndf*2) x 16 x 16
            Conv2d(ndf * 2, ndf * 4, 4, 2, 1, bias=False),
            BatchNorm2d(ndf * 4),
            LeakyReLU(0.2, inplace=True),
            # state size. (ndf*4) x 8 x 8
            Conv2d(ndf * 4, ndf * 8, 4, 2, 1, bias=False),
            BatchNorm2d(ndf * 8),
            LeakyReLU(0.2, inplace=True),
            # state size. (ndf*8) x 4 x 4
            Conv2d(ndf * 8, 1, 2, 1, 0, bias=False),
            Sigmoid()
        ) 

    def forward(self, X):
        x = self.main(X)     
        return x


# -------------------------------------------------------
# Initializers for model encoders with various depths
# -------------------------------------------------------

def genresnet18(**kwargs):
    """Constructs a generator based on a ResNet-18 model.
    """
    return Generator(resnetblocks.EresNetBasicBlock, resnetblocks.DresNetBasicBlock, [2, 2, 2, 2], **kwargs)

def genresnet34(**kwargs):
    """Constructs a generator based on a ResNet-34 model.
    """
    return EresNet(resnetblocks.EresNetBasicBlock, [3, 4, 6, 3], **kwargs)

def genresnet50(**kwargs):
    """Constructs a generator based on a ResNet-50 model.
    """
    return EresNet(resnetblocks.EresNetBottleneck, [3, 4, 6, 3], **kwargs)

def genresnet101(**kwargs):
    """Constructs a generator based on a ResNet-101 model.
    """
    return EresNet(resnetblocks.EresNetBottleneck, [3, 4, 23, 3], **kwargs)

def genresnet152(**kwargs):
    """Constructs a generator based on a ResNet-152 model.
    """
    return EresNet(resnetblocks.EresNetBottleneck, [3, 8, 36, 3], **kwargs)

# -------------------------------------------------------
# Initializers for model decoders with various depths
# -------------------------------------------------------

def disresnet18(**kwargs):
    """Constructs a discriminator based on a ResNet-18 model decoder.
    """
    return Discriminator(resnetblocks.EresNetBasicBlock, resnetblocks.DresNetBasicBlock, [2, 2, 2, 2], **kwargs)

def disresnet34(**kwargs):
    """Constructs a discriminator based on a ResNet-34 model decoder.
    """
    return Discriminator(resnetblocks.DresNetBasicBlock, [3, 4, 6, 3], **kwargs)

def disresnet50(**kwargs):
    """Constructs a discriminator based on a ResNet-50 model decoder.
    """
    return Discriminator(resnetblocks.DresNetBottleneck, [3, 4, 6, 3], **kwargs)

def disresnet101(**kwargs):
    """Constructs a discriminator based on a ResNet-101 model decoder.
    """
    return Discriminator(resnetblocks.DresNetBottleneck, [3, 4, 23, 3], **kwargs)

def disresnet152(**kwargs):
    """Constructs a discriminator based on a ResNet-152 model decoder.
    """
    return Discriminator(resnetblocks.DresNetBottleneck, [3, 8, 36, 3], **kwargs)
