import importlib
import matplotlib as mpl
import matplotlib.font_manager as font_manager
import os
from matplotlib import rcParams
from tqdm import tqdm
import warnings
import sys
warnings.filterwarnings("ignore")

MATPLOT_STYLE = './code/mplrc'
FONT_FOLDER = '/Users/alelouis/Library/Fonts'
FONT = 'JetBrains Mono'
IGNORES = ['__pycache__', '.ipynb_checkpoints']
STATIC_PATH = './static/images/'


def ignore(f, ignores):
    return not any([ignore in f.path for ignore in ignores])


mpl.rc_file(MATPLOT_STYLE)
font_dir = [FONT_FOLDER]
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)
rcParams['font.family'] = FONT

if len(sys.argv) == 2:
    module_name = sys.argv[1]
    files = [f'./code/{module_name}']
else:
    files = [f.path for f in os.scandir('./code/') if f.is_dir() and ignore(f, IGNORES)]

pbar = tqdm(files)
for file in pbar:
    module_name = file.split('/')[-1]
    static_module_path = f"{STATIC_PATH}{module_name}"
    pbar.set_description(f"Generating figures for {module_name}")
    module = importlib.import_module(f'code.{module_name}.figures')
    module.generate(static_module_path)
