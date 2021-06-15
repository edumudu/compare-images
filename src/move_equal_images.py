import re

from os import listdir, rename
from os.path import isfile, join, exists
from PIL import Image
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
  hashes = []

  print(colors.BLUE, f'\n {total_files} files finded \n', colors.RESET)

  for file in tqdm(onlyfiles, desc='Hashing images'):
    full_path = join(source_dir, file)
    img = Image.open(full_path)
    hashes.append(image_to_hash(img))

  bar = tqdm(total=total_interations, desc='Comparing images')
  i = total_files

  while i > 0:
    i -= 1

    hashA = hashes[i]

    j = i

    while j > 0:
      j -= 1
      delta = 1

      hashB = hashes[j]

      if hashA == hashB:
        fileB = onlyfiles[j]
        filenameB = join(source_dir, fileB)
        filesToRemove.add((filenameB, fileB))
        
        del onlyfiles[j]
        del hashes[j]
        i -= 1
        delta += i

      bar.update(delta)

  bar.close()
  print(colors.WARNING, '\n', len(filesToRemove), 'Files was marked to been removed \n', colors.RESET)

  for oldPath, filename in filesToRemove:
    newPath = join(target_dir, filename)

    rename(oldPath, pick_new_name(target_dir, filename) if exists(newPath) else newPath)
    print(colors.FAIL, 'Moved "' + filename +'" to Trash', colors.RESET)
