from os.path import join, exists

def pick_new_name(dir, filename, count = 1):
  new_path = join(dir, filename)

  return new_path if exists(new_path) else pick_new_name(dir, f'{filename}-{count}', count + 1)