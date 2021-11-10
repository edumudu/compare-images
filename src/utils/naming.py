import re

from os.path import join, exists

def pick_new_name(dir, filename):
  new_path = join(dir, filename)
  get_count_regex = r'_(\d+)(?!.*\d)'

  search_result = re.search(get_count_regex, filename)
  current_count = int(search_result.group(1)) + 1 if search_result else 1
  new_filename = re.sub(get_count_regex, f'_{current_count}', filename) if search_result else re.sub(r'(\.+)(?!.*\.)', f'_{current_count}.', filename)

  return pick_new_name(dir, new_filename) if exists(new_path) else new_path