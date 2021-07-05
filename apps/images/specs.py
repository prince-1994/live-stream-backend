from imagekit import ImageSpec
from imagekit.processors import ResizeToFill

class Thumbnail(ImageSpec):
    processors = [ResizeToFill(100, 100)]
    format = 'JPEG'
    options = {'quality': 60}