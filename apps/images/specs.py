from imagekit import ImageSpec
from imagekit.processors import ResizeToFit
from pilkit.processors.resize import ResizeToFill

class Image36x36(ImageSpec):
    processors = [ResizeToFill(36, 36)]
    format = 'PNG'
    options = {'quality': 100}

class Image48x48(ImageSpec):
    processors = [ResizeToFill(48, 48)]
    format = 'PNG'
    options = {'quality': 100}

class Image64x64(ImageSpec):
    processors = [ResizeToFill(64, 64)]
    format = 'PNG'
    options = {'quality': 100}

class Image128x128(ImageSpec):
    processors = [ResizeToFill(128, 128)]
    format = 'PNG'
    options = {'quality': 100}

class Image256x256(ImageSpec):
    processors = [ResizeToFill(256, 256)]
    format = 'PNG'
    options = {'quality': 100}

class Image512x512(ImageSpec):
    processors = [ResizeToFill(512, 512)]
    format = 'PNG'
    options = {'quality': 100}

class Image1500x400(ImageSpec):
    processors = [ResizeToFill(1500, 400)]
    format = 'PNG'
    options = {'quality': 100}

class Image1600x900(ImageSpec):
    processors = [ResizeToFill(1600, 900)]
    format = 'PNG'
    options = {'quality': 100}

class Image320x180(ImageSpec):
    processors = [ResizeToFill(320, 180)]
    format = 'PNG'
    options = {'quality': 100}