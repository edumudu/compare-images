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

  files = [filename for filename in listdir(source_dir) if isfile(join(source_dir, filename))]
  files = [file for file in files if re.search(f"^.*?\.({ext or SUPPORTED_FILES_EXTENSIONS})$", file)]

  total_files = len(files)
  total_interations = (total_files * (total_files - 1)) / 2

  files_to_remove = set()
  hashes = []

  for file in tqdm(files, desc='Hashing images'):
    full_path = join(source_dir, file)
    img = Image.open(full_path)
    hashes.append(image_to_hash(img))

  bar = tqdm(total=total_interations, desc='Comparing images')
  i = total_files

  while i > 0:
    i -= 1

    hash_a = hashes[i]

    j = i

    while j > 0:
      j -= 1
      delta = 1

      hash_b = hashes[j]

      if hash_a == hash_b:
        file_b = files[j]
        filename_b = join(source_dir, file_b)
        files_to_remove.add((filename_b, file_b))
        
        del files[j]
        del hashes[j]
        i -= 1
        delta += i

      bar.update(delta)

  bar.close()
  print(colors.WARNING, '\n', len(files_to_remove), 'Files was marked to been removed \n', colors.RESET)

  for old_path, filename in tqdm(files_to_remove, desc="Moving files"):
    new_path = join(target_dir, filename)

    rename(old_path, pick_new_name(target_dir, filename) if exists(new_path) else new_path)
