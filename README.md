# Image-Maker
A Python based program that turns images into an image

!!! This is not the best code for this but it works !!!


# Setup - .EXE (Easy)

VirusTotal Scan: https://www.virustotal.com/gui/file/a3c8182fd163397d3b58fb1eafae388ef7bfe1c1121c8e9d4f3ab6a9bfb6fe41/detection

The EXE file is converted from the PY file using auto-py-to-exe. auto-py-to-exe packages all imported libraries in the project to the EXE file which is why the file is over 200 MB and can therfore not be uploaded to GitHub.

1. Download the EXE file from https://mega.nz/#!4NUE1aiJ!LiL9r2uNxJJg6NGdYbs64AbxMkhHND819NgxmP87FRE
2. Place ImageMaker.exe and open CMD in that folder
3. Type "ImageMaker.exe -s" for setup
4. Place your small images in Collection


# Setup - .PY (Hard)

1. Download Python 3.6 and install PILLOW
2. Download ImageMaker.py from the project
3. Type "python ImageMaker.exe -s" for setup
4. Place your small images in Collection


# Syntax

(python) ImageMaker.exe [Image Name] [Images in width] [Images in height] [Output width]

[Image Name] - Path to primary image

[Images in width] - Small images in width

[Images in height] - Small images in height

[Output width] - Width of output image


# Example

"ImageMaker.exe img.jpg 200 200 8000"
