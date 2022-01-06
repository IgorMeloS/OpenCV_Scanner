# Scanner with Python and OpenCV

Practical scanner with Python and OpenCV. Following the source code by [PyImageSearch](https://www.pyimagesearch.com/2014/09/01/build-kick-ass-mobile-document-scanner-just-5-minutes/).

## About the Scanner

The scan module is built to propose you many options of scanning. Examples of scanning are one single page scan, multiple page scan. As well, color scan, black and white scan. You can choose which format you want to save your scan, pdf or jpg. The script file `scan.py` accepts some arguments that help us to understand the scan module. Let’s see.

- `-mlt`. Multiple scan mode, by default `False`, with you want more than one page, pass `True`.

- `-m`. Color mode of the scan, by default color (`c`). Options black and white (`bw`) or both (`cbw`).

- `-s`. Save mode, by default `pdf`. You can pass `jpg` or `b` if you want both formats.

- `-op`. One pdf file by default `True`. Must be passed when using multiple scan and pdf save mode. If `False`, each scanned image will be saved in a different .pdf file.

## Usage

First of all, verify if you have installed the requirements. The root structure of the scan module

```
scan
│   transform.py
│   scan.py    
│
└───input
│   
└───scan_31_12_2021_13:04:13
    │   scan.pdf
    │   ...
    └───originals
```

To use the scanner, the first step you must do is to place your images inside the folder ```input```, in the root directory. After the scanning process, the scanner generates a folder named as `scan_DD_MM_YY_H:M:S` to save the scans. In addition, every you scan, the originals files are removed into a folder called `originals`, in this way the folder `input` is always kept empty.

Open the terminal in the root directory `scan` and follow the instructions.

### Scanning one single page

- Considering you have one file to be scanned, run this code

`python scan.py`

this returns one pdf file of an image in color space

- If you want to save in jpg format, run the follow code

`python scan.py -s jpg`

- If you want to save in jpg and pdf

`python scan.py -s b`

- If you want in black and white space

`python scan.py -m bw`

- If you want in black and white space and jpg format

`python scan.py -m bw -s jpg`

- If you want in the color space, black and white, jpg and pdf

`python scan.py -m cbw -s b`

In this case, we have a total of four scanned images. There are others possibilities for one-page scan, feel free to try.

### Scanning multiple pages

In the case you have two or more images, the scanner can also help you.

- Considering you have two images and, you want to scanner them into a single pdf file, the follow code provide what you want

`python scan.py -mlt True`

- If you want to save your two scanned images into two different pdf files

`python scan.py -mlt True -op False`

- If you want to save in jpg format

`python scan.py -mlt True -s jpg`

- If you want to save in jpg and pdf formats

`python scan.py -mlt True -s b` or `python scan.py -mlt True -s b -op False`

- If you want to save in jpg and pdf formats, color space and black and white

`python scan.py -mlt True -m cbw -s b` (the results in the [folder](https://github.com/IgorMeloS/OpenCV_Scanner/tree/main/scan/scan_31_12_2021_13:04:13) was generated with this code).

or

`python scan.py -mlt True -m cbw -s b -op False`

Feel free to try other combinations of functions.

## About source images

One limitation of this approach is the need of good input image. As we consider the edge detection to find the contours and then, find the four corner points, images with a complex background can returns a poor result. Avoid also images with shadows. When using this scanner with OpenCV, try to have images as these ones

 <img src="https://github.com/IgorMeloS/OpenCV_Scanner/blob/main/images/doc.jpg" width="450"> <img src="https://github.com/IgorMeloS/OpenCV_Scanner/blob/main/images/IMG_0983.jpeg" width="450">


## Results

Some examples, a color image and black and white.

<img src="https://github.com/IgorMeloS/OpenCV_Scanner/blob/main/scan/scan_31_12_2021_13:04:13/scan_1.jpg" width="450"> <img src="https://github.com/IgorMeloS/OpenCV_Scanner/blob/main/scan/scan_31_12_2021_13:04:13/scan_bw_1.jpg" width="450">


**Feel free to make suggestions, critics and new ideas**.
