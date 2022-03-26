

import sys
from argparse import ArgumentParser
import io_utils

def parse_args():
    parser = ArgumentParser(description="CLI for bpimage library")
    parser.add_argument('source', help="source image file")
    parser.add_argument('-o', '--output', help='destination image file')
    parser.add_argument('-d','--debug', action='store_true', help='creates a temporary image and displays using the default image viewer')

    if len(sys.argv) < 2:
        parser.print_help(sys.stderr)
        exit(1)
        
    return parser.parse_args()

def process_img(args):
    img = io_utils.open(args.source)

    if(args.output):
        io_utils.save(img, args.output)

    if(args.debug):
        io_utils.show(img)

def main():
    args = parse_args()

    try:
        process_img(args)
    except (io_utils.ImageOpenError, io_utils.ImageSaveError) as e: 
        return str(e)

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        sys.exit(f'Unexpected exception: {str(e)}')