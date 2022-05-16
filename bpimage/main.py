
import sys
from argparse import ArgumentParser
import io_utils
import filters
import transform

# todo
# decorator to validate img input
# deprecate PIL in io_utils?
# accept arguments for actions
# ig style filters? 


# sobel filter
# requirements.txt
# add setup.py for end users
# handling keyboard interrupt in c?
# compiling library/make file? 
# add convovle error / affine error


# transform rotate / shear / resize / thumbnail, tint, black and white, color filters

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


def parse_args():
    parser = ArgumentParser(description="CLI for bpimage library")
    parser.add_argument('source', help="source image file")
    parser.add_argument('-o', '--output', help='destination image file')
    parser.add_argument('-a', '--action', choices=ACTIONS.keys(), nargs="+")
    parser.add_argument('-d', '--debug', action='store_true',
                        help='creates a temporary image and displays using the default image viewer')

    # if no args provided, output the help message
    if len(sys.argv) < 2:
        parser.print_help(sys.stderr)
        exit(1)

    return parser.parse_args()


def process_img(args):
    img = io_utils.open(args.source)

    if args.action:
        for action in args.action:
            img = ACTIONS[action](img)

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
