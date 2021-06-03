# filter.py

import getopt
import sys

import image


def _output_help_text():
    print("Arguments:")
    print(" source_image -> source image given as path")
    print(" output_image -> output image given as path")
    print("Options:")
    print(" --gray_scale -> to convert the image to black and white")
    print(" --overlay -> to overlay a given image on top of the source")
    print(" --rotate -> to rotate image by N degrees")
    sys.exit()


def _validate_arguments_and_options(args: list):

    # Validating arguments
    # First element in args list is the name of python script(filter.py).
    # Arguments starts from second element.
    args = args[1:]

    # If --help or -h in arguments, print help text
    for arg in args:
        if arg in ["-h", "--help"]:
            _output_help_text()
            return None, None, None

    # Validating options
    try:
        options, values = getopt.getopt(
            args[0:], "o:r:g", ["overlay=", "rotate=", "gray_scale"]
        )
    except getopt.GetoptError as e:
        raise SyntaxError(e)

    if len(values) == 2:
        pass
    elif len(values) == 1:
        raise SyntaxError("Missing required argument 'output_image'")
    elif len(values) == 0:
        raise SyntaxError(
            "Missing required arguments 'source_image' and 'output_image'"
        )

    return values[0], values[1], options


def main():
    args = sys.argv

    (
        source_image,
        output_image,
        options,
    ) = _validate_arguments_and_options(args)

    # Create an Image instance object from Source Image
    img = image.Image(source_image)
    if options:
        for currentOption, currentValue in options:
            if currentOption in ["-o", "--overlay"]:
                img.overlay(currentValue)
            elif currentOption in ["-r", "--rotate"]:
                img.rotate(currentValue)
            elif currentOption in ["-g", "--gray_scale"]:
                img.gray_scale()
    img.save(output_image)


if __name__ == "__main__":
    main()
