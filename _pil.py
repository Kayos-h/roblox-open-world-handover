import sys
print(sys.version)
try:
    import PIL
    from PIL import Image
    print("Pillow", PIL.__version__)
except Exception as e:
    print("no Pillow:", e)
