from PIL import Image

# https://stackoverflow.com/a/49692185/12734929
def image_to_hash(img):
  simplified_image = img.resize((10, 10), Image.ANTIALIAS).convert('L')

  pixel_data = list(simplified_image.getdata())
  avg_pixel = sum(pixel_data) / len(pixel_data)

  bits = "".join(['1' if (px >= avg_pixel) else '0' for px in pixel_data])

  return str(hex(int(bits, 2)))[2:][::-1].upper()
