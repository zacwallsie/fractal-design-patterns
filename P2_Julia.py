import torch
import numpy as np
import matplotlib.pyplot as plt

# Device Config -> mps backend does not support complex floating numbers
device = torch.device('cpu')

# Using Numpy to create a 2D array of complex numbers [-2,2]x[-2,2]
Y, X = np.mgrid[-1.3:1.3:0.0003, -2:1:0.0003]

# Loading in PyTorch tensors
x = torch.Tensor(X)
y = torch.Tensor(Y)
z = torch.complex(x, y)
zs = z.clone()
ns = torch.zeros_like(z)

# Transferring to the GPU device
z = z.to(device)
zs = zs.to(device)
ns = ns.to(device)

# Julia Set
# Define a constant c for the Julia set (you can experiment with different values)
c_real = torch.tensor(-0.7)
c_imag = torch.tensor(0.27015)
c = torch.complex(c_real, c_imag).to(device)

for i in range(200):
    # Computing new values of z: z^2 + c
    zs_ = zs * zs + c

    # Test for Divergence
    not_diverged = torch.abs(zs_) < 4.0

    # Update variables to compute
    ns += not_diverged
    zs = zs_

fig = plt.figure(figsize=(16,10))

def Process_Fractal(a):
    """
    Display an Array of iteration counts as a colorful picture of a fractal.
    """
    a_cyclic = (6.28*a/20.0).reshape(list(a.shape)+[1])
    img = np.concatenate([10+20*np.cos(a_cyclic),
                            30+50*np.sin(a_cyclic),
                            155-80*np.cos(a_cyclic)], 2)
    img[a==a.max()] = 0
    a = img
    a = np.uint8(np.clip(a, 0, 255))
    return a
    
plt.imshow(Process_Fractal(ns.cpu().numpy()))
plt.tight_layout(pad=0)
plt.show()
