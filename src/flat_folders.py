from os import listdir, rename, rmdir
from os.path import isdir, join, exists, basename
from tqdm import tqdm

from .utils.naming import pick_new_name
from .constants.colors import colors

def flat_folder(dirPath, targetDir):
  if not exists(dirPath): return print(colors.FAIL, f'The dir "{dirPath}" not exists', colors.RESET)

  paths = listdir(dirPath)

  for path in tqdm(paths):
    full_path = join(dirPath, path)

    if(isdir(full_path)):
      flat_folder(full_path, targetDir)
      rmdir(full_path)
    else:
      rename(full_path, pick_new_name(targetDir, f'{basename(dirPath)}-{path}'))

  print(colors.GREEN, f'\n{len(paths)} files was successfuly moved!', colors.RESET)


def flat_folders(sourceDir, *args):
  if not exists(sourceDir): return print(colors.FAIL, 'The source dir not exists', colors.RESET)

  flat_folder(sourceDir, sourceDir)