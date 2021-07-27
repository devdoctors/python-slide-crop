# python-slide-crop
Crops and exports slide images

### Supports the following slide formats
(Uses the OpenSlide library)
* Aperio (.svs, .tif)
* Hamamatsu (.ndpi, .vms, .vmu)
* Leica (.scn)
* MIRAX (.mrxs)
* Philips (.tiff)
* Sakura (.svslide)
* Trestle (.tif)
* Ventana (.bif, .tif)
* Generic tiled TIFF (.tif)

## Getting started
This script was created in python 3 with the following dependencies:

### Dependencies
1. OpenSlide (https://openslide.org)
2. OpenCV2 (https://opencv.org)
3. Numpy

## Usage
1. python crop.py [filename] [extension]
2. drag to select area for export
3. press ENTER(RETURN) to export image
4. press ESC to close application
