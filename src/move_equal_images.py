import re
import itertools

from os import listdir, rename
from os.path import isfile, join, exists
from PIL import Image, ImageChops
from tqdm import tqdm

from .utils.naming import pick_new_name
from .utils.hashing import image_to_hash
from .constants.colors import colors

SUPPORTED_FILES_EXTENSIONS = 'png|jpg|jpeg'

def move_equal_images(source_dir, target_dir, ext = None):
  if not exists(source_dir): return print(colors.FAIL, 'The source dir not exists', colors.RESET)
  if not exists(target_dir): return print(colors.FAIL, 'The target dir not exists', colors.RESET)

  onlyfiles = [filename for filename in listdir(source_dir) if isfile(join(source_dir, filename))]
  onlyfiles = [file for file in onlyfiles if re.search(f"^.*?\.({ext or SUPPORTED_FILES_EXTENSIONS})$", file)]

  total_files = len(onlyfiles)
  total_interations = (total_files * (total_files - 1)) / 2

  filesToRemove = set()
  bar = tqdm(total=total_interations)

  i = total_files

  while i > 0:
    i -= 1

    fileA = onlyfiles[i]
    filenameA = join(source_dir, fileA)
    imgA = Image.open(filenameA)
    hashA = image_to_hash(imgA)

    j = i

    while j > 0:
      j -= 1
      delta = 1

      fileB = onlyfiles[j]
      filenameB = join(source_dir, fileB)
      imgB = Image.open(filenameB)
      hashB = image_to_hash(imgB)

      if(hashA == hashB):
        filesToRemove.add((filenameB, fileB))
        i -= 1
        delta += i

      bar.update(delta)

  bar.close()
  print(colors.WARNING, '\n', len(filesToRemove), 'Files was marked to been removed \n', colors.RESET)

  for oldPath, filename in filesToRemove:
    newPath = join(target_dir, filename)

    rename(oldPath, pick_new_name(target_dir, filename) if exists(newPath) else newPath)
    print(colors.FAIL, 'Moved "' + filename +'" to Trash', colors.RESET)
