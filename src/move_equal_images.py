import re
import itertools

from os import listdir, rename
from os.path import isfile, join, exists
from PIL import Image, ImageChops
from tqdm import tqdm

from .utils.naming import pick_new_name
from .constants.colors import colors

SUPPORTED_FILES_EXTENSIONS = 'png|jpg|jpeg'

def move_equal_images(source_dir, target_dir, ext = None):
  if not exists(source_dir): return print(colors.FAIL, 'The source dir not exists', colors.RESET)
  if not exists(target_dir): return print(colors.FAIL, 'The target dir not exists', colors.RESET)

  onlyfiles = [filename for filename in listdir(source_dir) if isfile(join(source_dir, filename))]
  onlyfiles = [file for file in onlyfiles if re.search(f"^.*?\.({ext or SUPPORTED_FILES_EXTENSIONS})$", file)]

  filesToRemove = set()
  bar = tqdm(total=len(list(itertools.combinations(onlyfiles, 2))))

  for fileA, fileB in itertools.combinations(onlyfiles, 2):
    filenameA = join(source_dir, fileA)
    filenameB = join(source_dir, fileB)

    imgA = Image.open(filenameA)
    imgB = Image.open(filenameB)

    diff = ImageChops.difference(imgA.convert('CMYK'), imgB.convert('CMYK'))

    removePayload = (filenameB, fileB)

    if(not diff.getbbox()):
      filesToRemove.add(removePayload)

    bar.update()

  bar.close()
  print(colors.WARNING, '\n', len(filesToRemove), 'Files was marked to been removed \n', colors.RESET)

  for oldPath, filename in filesToRemove:
    newPath = join(target_dir, filename)

    rename(oldPath, pick_new_name(target_dir, filename) if exists(newPath) else newPath)
    print(colors.FAIL, 'Moved "' + filename +'" to Trash', colors.RESET)
