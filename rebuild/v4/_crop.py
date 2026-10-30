import sys
from PIL import Image
src, dst, x0, y0, x1, y1 = sys.argv[1], sys.argv[2], *map(int, sys.argv[3:7])
im = Image.open(src).convert('RGB')
print('source size', im.size)
im.crop((x0, y0, x1, y1)).save(dst)
print('cropped', (x0, y0, x1, y1), '->', dst)
