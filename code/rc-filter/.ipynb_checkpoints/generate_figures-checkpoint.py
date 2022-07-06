import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import rcParams
import matplotlib.font_manager as font_manager

folder = "rc-filter"
static_path = f"./static/images/{folder}"

mpl.rc_file('mplrc')

font_dir = ['/Users/alelouis/Library/Fonts']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)

rcParams['font.family'] = 'JetBrains Mono'