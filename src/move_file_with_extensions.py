import re

from os import listdir, rename
from os.path import isfile, join, exists
from tqdm import tqdm

from .utils.naming import pick_new_name
from .constants.colors import colors

def move_files(sourceDir, targetDir, ext = None):
  if not ext: return print(colors.FAIL, 'A target extension(s) is required to move the files', colors.RESET)
  if not exists(sourceDir): return print(colors.FAIL, 'The source dir not exists', colors.RESET)
  if not exists(targetDir): return print(colors.FAIL, 'The target dir not exists', colors.RESET)

  files = [filename for filename in listdir(sourceDir) if isfile(join(sourceDir, filename))]
  files_to_move = [file for file in files if re.search('^.*?\.(' + ext + ')$', file)]

  for file in tqdm(files_to_move):
    oldName = join(sourceDir, file)
    newName = join(targetDir, file)

    rename(oldName, pick_new_name(targetDir, file) if exists(newName) else newName)

  print(colors.GREEN, f'\n{len(files_to_move)} files was successfuly moved!', colors.RESET)
