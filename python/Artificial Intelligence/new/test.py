

import numpy as np
import skimage.measure

a = np.zeros((26, 26))
print(a.shape)
print(skimage.measure.block_reduce(a, (2,2), np.max))