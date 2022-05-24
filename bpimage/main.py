
import sys
from argparse import ArgumentParser
import io_utils
import filters
import transform
import color

# todo
# accept arguments for actions
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
    'boxblur': filters.boxblur,
    'gaussian_blur': filters.gaussian_blur,
    'motion_blur': filters.motion_blur,
    'sharpen': filters.sharpen,
    'outline': filters.outline,
    'emboss': filters.emboss,
    'smooth': filters.smooth,
    'flipv': transform.flipv,
    'fliph': transform.fliph,
    'rotate90': transform.rotate90,
    'rotate': transform.rotate,
    'rescale': transform.rescale,
    'shear': transform.shear
}

ACTIONS2 = {
    'rgb2gray': {
        'args': {
            'action': 'store_const',
            'help': 'Converts the image to Grayscale, modifying the shape of an image from RGB (w,h,3) to grayscale (w,h,1).',
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
    'contrast': {
        'args': {
            'help': 'Increase or decrease the contrast of the image based on the strength (%(type)s). A value of 0.0 will result in a gray image, 1.0 gives the original image.',
            'nargs': 1,
            'type': float,
            'metavar': 'strength'
        },
        'command': color.contrast
    },
    'invert': {
        'args': {
            'action': 'store_const',
            'help': 'Invert the colors of the image, producing a negative.',
            'const': []
        },
        'command': color.invert
    },
    'saturation': {
        'args': {
            'help': 'Increase or decrease the saturation of the image based on the strength (%(type)s). A value of 0.0 will result in a black and white image, 1.0 gives the original image.',
            'nargs': 1,
            'type': float,
            'metavar': 'strength'
        },
        'command': color.saturation
    }
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

    for key, value in ACTIONS2.items():
        if (action_args := getattr(args, key)) is not None:
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
