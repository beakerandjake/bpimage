
import sys
from argparse import ArgumentParser
import io_utils
import bpimage

# todo 
# allow multiple filters, and execute them in a loop piping output of one to input of next
# output file with before/after for debigging
# sobel filter
# add setup.py for end users
# add convovle error
# handling keyboard interrupt in c?

# convovle.py, transform (rotate, flip), shear, resize / thumbnail, tint, black and white, color filters

def parse_args():
    parser = ArgumentParser(description="CLI for bpimage library")
    parser.add_argument('source', help="source image file")
    parser.add_argument('-o', '--output', help='destination image file')
    parser.add_argument('-d','--debug', action='store_true', help='creates a temporary image and displays using the default image viewer')
    # filters
    parser.add_argument('-b','--blur', action='store_true', help='blurs the source image')
    parser.add_argument('-s','--sharpen', action='store_true', help='sharpen the source image')
    parser.add_argument('-out','--outline', action='store_true', help='edge detect the source image')
    parser.add_argument('-e','--emboss', action='store_true', help='emboss the source image')
    parser.add_argument('-m','--motionblur', action='store_true', help='motion blur the source image')
    parser.add_argument('-sm','--smooth', action='store_true', help='smooth the source image')

    if len(sys.argv) < 2:
        parser.print_help(sys.stderr)
        exit(1)
        
    return parser.parse_args()

def process_img(args):
    img = io_utils.open(args.source)

    if(args.blur):
        img = bpimage.boxblur(img,3)
    
    if(args.sharpen):
        img = bpimage.sharpen(img)
    
    if(args.outline):
        img = bpimage.outline(img)
    
    if(args.emboss):
        img = bpimage.emboss(img)

    if(args.motionblur):
        img = bpimage.motion_blur(img)

    if(args.smooth):
        img = bpimage.smooth(img)

    if(args.output):
        io_utils.save(img, args.output)

    if(args.debug):
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