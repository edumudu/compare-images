import argparse

from os import getcwd
from os.path import join

from src.move_equal_images import move_equal_images
from src.move_file_with_extensions import move_files
from src.flat_folders import flat_folders

parser = argparse.ArgumentParser()

parser.add_argument('action', help='Action to be executed', choices=['compare', 'move', 'flat'])
parser.add_argument('sourcePath', help='Dir path to be read')
parser.add_argument('targetPath', help='Dir path to move files')

parser.add_argument('--ext', help='Target extensions')

args = parser.parse_args()

source_dir = join(getcwd(), args.sourcePath)
target_dir = join(getcwd(), args.targetPath)

actions = {
  'compare': lambda *args: move_equal_images(*args),
  'move': lambda *args: move_files(*args),
  'flat': lambda *args: flat_folders(*args)
}

handler = actions.get(args.action)

handler(source_dir, target_dir, args.ext)
