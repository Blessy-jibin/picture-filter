# About this project

A command-line script that applies 1 or more filters to an image and saves it as a new file. 

The filters should be:

1. `gray_scale` convert the image to black and white.
2. `overlay` overlay a given image on top of the source.
3. `rotate` rotate N degrees. (no need for resizing/cropping)
4. Optionally, make up your own filter. Not required.

Other requirements:

* All parameters should be given in one line. (no interactive approach using `input()`)
* Each filter should be optional. 
* The order of filters is important since we want to be able to control if the overlay will become black and white or not. 
* The source image should be given as a filename on the command line.
* The overlay image should also be given as a filename on the command line and should be a transparent png.
* The number of degrees should be given on the command line.
* The output file should be given as a filename on the command line. (Support saving as png and jpg)
* Allow applying a filter more than once. (for example: gray_scale > rotate > overlay > rotate)

### How to use script 
1. cd to the project folder
2. Run 'bash env.sh' on command to create virtual environment.
3. Run 'source .venv/filter/bin/activate'
4. Run 'python3 -m filter options source_image output_image'

### How to run test 
1. Run 'bash env.sh' on command to create virtual environment, if virtual environment is not present.
2. Run 'source .venv/filter/bin/activate'
3. Run 'pytest test.py'
