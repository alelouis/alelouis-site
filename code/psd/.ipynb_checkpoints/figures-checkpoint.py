import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm


def generate(path):
    pbar = tqdm(total=6, leave=False)
    plt.figure(figsize=(6, 3))
    plt.plot(np.hamming(256))
    plt.xlabel('Samples')
    plt.ylabel('Amplitude')
    plt.savefig(f'{path}/ham.svg', dpi=72, transparent=True, bbox_inches='tight')
    pbar.update(1)
