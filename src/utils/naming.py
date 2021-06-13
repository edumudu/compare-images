from os.path import join, exists

def pick_new_name(dir, filename, count = 1):
  new_path = join(dir, filename)
  file, _, file_ext = filename.rpartition('.')

  return pick_new_name(dir, f'{file}-{count}.{file_ext}', count + 1) if exists(new_path) else new_path