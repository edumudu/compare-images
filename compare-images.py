import pathlib
import sys
import re
import itertools
from os import listdir, getcwd, rename
from os.path import isfile, join
from PIL import Image, ImageChops
from tqdm import tqdm

class bcolors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    RESET = '\x1b[0m'

_, dirPathToRead = sys.argv

dirPathToRead = join(getcwd(), dirPathToRead)
dirPathTrash = join(pathlib.Path(__file__).parent.absolute(), 'trash')

onlyfiles = [filename for filename in listdir(dirPathToRead) if isfile(join(dirPathToRead, filename))]
onlyfiles = list(filter(lambda filename: re.search("^.*?\.(png|jpg|jpeg)$", filename), onlyfiles))

filesToRemove = set()
bar = tqdm(total=len(list(itertools.combinations(onlyfiles, 2))))

for fileA, fileB in itertools.combinations(onlyfiles, 2):
  filenameA = join(dirPathToRead, fileA)
  filenameB = join(dirPathToRead, fileB)

  imgA = Image.open(filenameA)
  imgB = Image.open(filenameB)

  diff = ImageChops.difference(imgA.convert('CMYK'), imgB.convert('CMYK'))

  removePayload = (filenameB, fileB)

  if(not diff.getbbox() and removePayload not in filesToRemove):
    # print(bcolors.BLUE, 'Marked to move to Trash: ' + fileB, bcolors.RESET)
    filesToRemove.add(removePayload)

  bar.update()

bar.close()
print(bcolors.WARNING, '\n', len(filesToRemove), 'Files was marked to been removed \n', bcolors.RESET)

for oldPath, filename in filesToRemove:
  rename(oldPath, join(dirPathTrash, filename))
  print(bcolors.FAIL, 'Moved "' + filename +'" to Trash', bcolors.RESET)