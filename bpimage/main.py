
import sys
from argparse import ArgumentParser
from xml.dom import WrongDocumentErr
import io_utils
import filters
import transform
import color

# todo
# accept arguments for actions
# spell check
# consistent comments / naming
# requirements.txt
# setup and compiling the c files for packaging.
#   compiling library/make file?
# error handling
# readme
#   make gifs showing rotation / skew resize / strengths?
# image sliders that show before and after?
# make public


# ig style filters?

ACTIONS = {
    'gaussian_blur': filters.gaussian_blur,
    'emboss': filters.emboss,
    'rotate': transform.rotate,
    'shear': transform.shear
}

ACTIONS2 = {

    'rgb2gray': {
        'args': {
            'action': 'store_const',
            'help': 'Converts the image to Grayscale.',
            'const': []
        },
        'command': color.rgb2grayscale
    },
    'gray2rgb': {
        'args': {
            'action': 'store_const',
            'help': 'Converts the shape of an image from grayscale (w,h,1) to RGB (w,h,3).',
            'const': []
        },
        'command': color.grayscale2rgb
    },
    'sepia': {
        'args': {
            'action': 'store_const',
            'help': 'Applies a sepia effect to the image.',
            'const': []
        },
        'command': color.sepia
    },
    'brightness': {
        'args': {
            'help': 'Increase or decrease the brightness of the image based on the strength (%(type)s). A value of 0.0 will result in a black image, 1.0 gives the original image.',
            'nargs': 1,
            'type': float,
            'metavar': 'strength'
        },
        'command': color.brightness
    },
    'invert': {
        'args': {
            'action': 'store_const',
            'help': 'Invert the colors of the image, producing a negative.',
            'const': []
        },
        'command': color.invert
    },
    'contrast': {
        'args': {
            'help': 'Increase or decrease the contrast of the image based on the strength (%(type)s). A value of 0.0 will result in a gray image, 1.0 gives the original image.',
            'nargs': 1,
            'type': float,
            'metavar': 'strength'
        },
        'command': color.contrast
    },
    'saturation': {
        'args': {
            'help': 'Increase or decrease the saturation of the image based on the strength (%(type)s). A value of 0.0 will result in a black and white image, 1.0 gives the original image.',
            'nargs': 1,
            'type': float,
            'metavar': 'strength'
        },
        'command': color.saturation
    },
    'flipv': {
        'args': {
            'action': 'store_const',
            'help': 'Flips the image across the vertical, from left to right.',
            'const': []
        },
        'command': transform.flipv
    },
    'fliph': {
        'args': {
            'action': 'store_const',
            'help': 'Flips the image across the horizontal, from bottom to top.',
            'const': []
        },
        'command': transform.fliph
    },
    'scale': {
        'args': {
            'help': 'Re-sizes the image uniformly based on a (non-zero) scale factor. A value of 1.0 returns the original image.',
            'nargs': 1,
            'type': float,
            'metavar': 'factor'
        },
        'command': transform.scale
    },







    'boxblur': {
        'args': {
            'help': 'Blurs each pixel by averaging all surrounding pixels extending radius pixels in each direction.',
            'nargs': 1,
            'type': int,
            'metavar': 'radius'
        },
        'command': filters.boxblur
    },
    'outline': {
        'args': {
            'help': 'Applies an edge detection kernel to the image.',
            'const': [],
            'action': 'store_const'
        },
        'command': filters.outline
    },
    'sharpen': {
        'args': {
            'help': 'Sharpens the image.',
            'const': [],
            'action': 'store_const'
        },
        'command': filters.sharpen
    },
    'sharpen': {
        'args': {
            'help': 'Sharpens the image.',
            'nargs': 1,
            'type': float,
            'metavar': 'strength'
        },
        'command': filters.sharpen
    },
    'boxblur': {
        'args': {
            'help': 'Blurs each pixel by averaging all surrounding pixels extending radius pixels in each direction.',
            'nargs': 1,
            'type': int,
            'metavar': 'radius'
        },
        'command': filters.boxblur
    },
    'gaussian': {
        'args': {
            'help': 'Applies a gaussian blur to the image. the image.',
            'const': [],
            'action': 'store_const'
        },
        'command': filters.gaussian_blur
    },
    'motionblur': {
        'args': {
            'help': 'Applies a motion blur to the image.',
            'const': [],
            'action': 'store_const'
        },
        'command': filters.motion_blur
    },
}

# action specify short name and full name.
# specify help, specify args.


def parse_args():
    parser = ArgumentParser(description="CLI for bpimage library")
    parser.add_argument('source', help="source image file")
    parser.add_argument('-o', '--output', help='destination image file')
    # parser.add_argument('-a', '--action', choices=ACTIONS.keys(), nargs="+")
    parser.add_argument('-d', '--debug', action='store_true',
                        help='creates a temporary image and displays using the default image viewer')

    for key, value in ACTIONS2.items():
        parser.add_argument(f'--{key}', **value['args'])

    # if no args provided, output the help message
    if len(sys.argv) < 2:
        parser.print_help(sys.stderr)
        exit(1)

    return parser.parse_args()


def process_img(args):
    img = io_utils.open(args.source)

    # print(vars(args))
    # print()
    # print()

    for key, value in ACTIONS2.items():
        # print('iterating:', key, 'value:', value)
        if (action_args := getattr(args, key)) is not None:
            # print(action_args)
            # print(value)
            # print()
            img = value['command'](img, *action_args)

    if args.output:
        io_utils.save(img, args.output)

    if args.debug:
        io_utils.show(img)


def main():
    args = parse_args()

    try:
        process_img(args)
    except (io_utils.ImageOpenError, io_utils.ImageSaveError, io_utils.ImageShowError) as e:
        return str(e)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit()
    # except Exception as e:
    #     sys.exit(f'Unexpected exception: {str(e)}')
