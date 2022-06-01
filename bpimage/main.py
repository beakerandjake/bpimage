
import sys
from argparse import ArgumentParser, Action, ArgumentTypeError
import collections.abc
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


class ParseMultipleTypes(Action):
    """Custom argparse.Action which supports multiple arguments with different types. 
    args are zipped with the types and each argument will be converted to its respective type.  
    """

    def __init__(self, types, *args, **kwargs):
        self._types = types
        super(ParseMultipleTypes, self).__init__(*args, **kwargs)

    def __call__(self, parser, args, values, option_string=None):
        setattr(args, self.dest, list(self._convert_types(values, parser)))

    def _convert_types(self, values, parser):
        for (arg, desired_type) in zip(values, self._types):
            try:
                yield desired_type(arg)
            except (ValueError, TypeError, ArgumentTypeError):
                parser.error(
                    f'argument --{self.dest}: invalid {desired_type.__name__} value: \'{arg}\'')


def str_to_bool(v):
    """Attempts to parse the string value as a boolean.
    https://stackoverflow.com/questions/15008758
    """
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise ArgumentTypeError('Boolean value expected.')


ACTIONS = {
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
            'help': 'Increase or decrease the brightness of the image based on the strength. A value of 0.0 will result in a black image, 1.0 gives the original image. (type:%(type)s)',
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
            'help': 'Increase or decrease the contrast of the image based on the strength. A value of 0.0 will result in a gray image, 1.0 gives the original image. (type:%(type)s)',
            'nargs': 1,
            'type': float,
            'metavar': 'strength'
        },
        'command': color.contrast
    },
    'saturation': {
        'args': {
            'help': 'Increase or decrease the saturation of the image based on the strength. A value of 0.0 will result in a black and white image, 1.0 gives the original image. (type:%(type)s)',
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
    'rotate90': {
        'args': {
            'help': 'Rotates the image counter-clockwise 90 degrees around the center n number of times (default:%(default)s, type:%(type)s).',
            'nargs': '?',
            'const': 1,
            'type': int
        },
        'command': transform.rotate90
    },
    'rotate': {
        'args': {
            'help': 'Rotates the image counter-clockwise by a specified angle around the center. If expand is set to true, the canvas size will be expanded to hold the rotated image. (types: float, bool)',
            'nargs': 2,
            'action': ParseMultipleTypes,
            'types': [float, str_to_bool],
            'metavar': ('angle', 'expand')
        },
        'command': transform.rotate
    },
    'scale': {
        'args': {
            'help': 'Re-sizes the image uniformly based on a (non-zero) scale factor. A value of 1.0 returns the original image. (type:%(type)s)',
            'nargs': 1,
            'type': float,
            'metavar': 'factor'
        },
        'command': transform.scale
    },
    'shear': {
        'args': {
            'help': 'Shears the image in the specified dimension. A shear_x or shear_y value of 1.0 does not modify that axis. (type: float, float, bool)',
            'nargs': 3,
            'action': ParseMultipleTypes,
            'types': [float, float, str_to_bool],
            'metavar': ('shear_x', 'shear_y', 'expand')
        },
        'command': transform.shear
    },
    # filters
    'boxblur': {
        'args': {
            'help': 'Blurs each pixel by averaging all surrounding pixels extending radius pixels in each direction. (default:%(default)s, type:%(type)s)',
            'nargs': '?',
            'type': int,
            'const': 1,
            'metavar': 'radius'
        },
        'command': filters.boxblur
    },
    'outline': {
        'args': {
            'help': 'Highlights edges of the image.',
            'const': [],
            'action': 'store_const'
        },
        'command': filters.outline
    },
    'sharpen': {
        'args': {
            'help': 'Sharpens the image. (type:%(type)s)',
            'nargs': 1,
            'type': float,
            'metavar': 'strength'
        },
        'command': filters.sharpen
    },
    'motionblur': {
        'args': {
            'help': 'Applies a motion blur to the image.',
            'const': [],
            'action': 'store_const'
        },
        'command': filters.motion_blur
    },
    'emboss': {
        'args': {
            'help': "Applies an emboss effect to the image. Supported direction values are 'u', 'd', 'l' and 'r' for up, down, left and right respectively. Strength determines the number of surrounding pixels to consider, larger values result in stronger highlights. (types: str, int)",
            'nargs': 2,
            'metavar': ('direction', 'strength'),
            'action': ParseMultipleTypes,
            'types': [str, int]
        },
        'command': filters.emboss
    },
    'gaussian': {
        'args': {
            'help': 'Applies a gaussian blur to the image. Radius controls the number of pixels to take in each direction. Sigma determines the strength of the blur.  (types: int, float)',
            'nargs': 2,
            'metavar': ('radius', 'sig'),
            'action': ParseMultipleTypes,
            'types': [int, float]
        },
        'command': filters.gaussian_blur
    }
}


def parse_args():
    parser = ArgumentParser(description="CLI for bpimage library")
    parser.add_argument('source', help="source image file")
    parser.add_argument('-o', '--output', help='destination image file')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='creates a temporary image and displays using the default image viewer')

    for key, value in ACTIONS.items():
        parser.add_argument(f'--{key}', **value['args'])

    # if no args provided, output the help message
    if len(sys.argv) < 2:
        parser.print_help(sys.stderr)
        exit(1)

    return parser.parse_args()


def process_img(args):
    img = io_utils.open(args.source)

    for key, value in ACTIONS.items():
        if (action_args := getattr(args, key)) is not None:
            if isinstance(action_args, collections.abc.Sequence):
                img = value['command'](img, *action_args)
            else:
                img = value['command'](img, action_args)

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
