
"""CLI for bpimage library.
"""
import sys
from argparse import ArgumentParser, Action, ArgumentTypeError
from pathlib import Path
import collections.abc
import io_utils
import filters
import transform
import color

# todo
# setup and compiling the c files for packaging.
#   compiling library/make file?
# readme
#   make gifs showing rotation / skew resize / strengths?
# image sliders that show before and after?
# make public


class ParseMultipleTypes(Action):
    """Custom argparse.Action which supports multiple arguments with different types. 
    args are zipped with the types and each argument will be converted to its respective type.  
    Needed to support nargs > 1 with different types, as argparse only supports one type.
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
    Can be used with argparse to support bool arguments.
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
    'color modifications': {
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
    },
    'image transformations': {
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
                'help': 'Rotates the image counter-clockwise 90 degrees around the center n number of times (default:%(const)s, type:%(type)s).',
                'nargs': '?',
                'const': 1,
                'type': int,
                'metavar': 'times'
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
                'help': 'Shears the image in the specified dimension. A shear_x or shear_y value of 0.0 will not shear that axis. If expand is set to true, the canvas size will be expanded to hold the rotated image. (type: float, float, bool)',
                'nargs': 3,
                'action': ParseMultipleTypes,
                'types': [float, float, str_to_bool],
                'metavar': ('shear_x', 'shear_y', 'expand')
            },
            'command': transform.shear
        }
    },
    'convolution filters': {
        'boxblur': {
            'args': {
                'help': 'Blurs each pixel by averaging all surrounding pixels extending radius pixels in each direction. (default:%(const)s, type:%(type)s)',
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
}


def _get_cli_args():
    parser = ArgumentParser(description='CLI for bpimage library. Performs image editing on RGB images.')
    parser.add_argument('source', help='source image file path', type=Path)

    # make user to choose to output to a file or to preview the image.
    output_group = parser.add_mutually_exclusive_group(required=True)
    output_group.add_argument('-d', '--dest', help='destination image file path', type=Path)
    output_group.add_argument('-p', '--preview', action='store_true',
                        help='creates a temporary image and displays using the default image viewer')

    # create each argument group and add all group commands.
    for group_key, group_value in ACTIONS.items():
        argument_group = parser.add_argument_group(group_key)
        for command_key, command_value in group_value.items():
            argument_group.add_argument(
                f'--{command_key}', **command_value['args'])

    # if no args provided, output the help message
    if len(sys.argv) < 2:
        parser.print_help(sys.stderr)
        exit(1)

    return parser.parse_args()


def _process_img(args):
    img = io_utils.open(args.source)

    # execute each command provided to generate the final image.
    for group in ACTIONS.values():
        for (command_key, command_args) in group.items():
            # if command was specified as an argument then invoke it. 
            if (action_args := getattr(args, command_key)) is not None:
                if isinstance(action_args, collections.abc.Sequence):
                    # ensure multiple args get unpacked.
                    img = command_args['command'](img, *action_args)
                else:
                    img = command_args['command'](img, action_args)

    if args.dest:
        io_utils.save(img, args.dest)

    if args.preview:
        io_utils.show(img)


def _main():
    args = _get_cli_args()

    try:
        _process_img(args)
    except (io_utils.ImageOpenError, io_utils.ImageSaveError, io_utils.ImageShowError) as e:
        return str(e)


if __name__ == '__main__':
    try:
        sys.exit(_main())
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        sys.exit(f'Unexpected exception: {str(e)}')
