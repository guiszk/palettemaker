from PIL import Image, ImageDraw, ImageFont
import argparse
import os, sys

#if(len(sys.argv) < 3):
#    print("{} <image file> <number of colors in palette [1-256]> <*palette output file>".format(sys.argv[0]))
#    sys.exit(1)

parser = argparse.ArgumentParser(description='Generate color palettes from images.')
parser.add_argument(dest='img', type=str, help="Image path")
parser.add_argument(dest='num', type=int, help="Number of colors in palette")
parser.add_argument('-o', '--output', type=str, help="Save color palette as image")
parser.add_argument('-e', '--embed', type=str, help="Embed palette in original image and write as new file")
args = parser.parse_args()

END = "\x1b[0m"
def RGB(RGBl, Foreground=True):
    FB_G = 38
    if Foreground != True:
        FB_G = 48
    return "\x1b[" + str(FB_G) + ";2;" + str(RGBl[0]) + ";" + str(RGBl[1]) + ";" + str(RGBl[2]) + "m"

def rgbhex(rgb):
    return '%02x%02x%02x' % tuple(rgb)

def getpalette(f, num, v=True):
    img = Image.open(f).convert("RGBA")
    q = img.quantize(colors=num, method=2)
    paletteout = []
    for i in [j for j in range(num*3) if j%3==0]:
        c = q.getpalette()[i:i+3]
        paletteout.append(c)
        if(v):
            print(RGB(c), "■■■■■■■", END, str("#" + rgbhex(c)))
    return paletteout
numcol = args.num

if(os.path.isfile(args.img)):
    pal = getpalette(args.img, numcol, v=True)
else:
    print("{} is not a valid file.".format(args.img))
    sys.exit(1)

def genpalette(w, h):
    img = Image.new("RGBA", (w, h))
    for i in range(numcol):
        dv = w/numcol
        shape = [(dv*i, 0), ((dv*i)+dv, h)]
        hx = "#" + rgbhex(pal[i])
        ImageDraw.Draw(img).rectangle(shape, fill=hx)
    return img

if(args.output):
    w, h = 640, 360
    im = genpalette(640, 360)
    im.save(args.output)
    print(str("Color palette saved at " + os.path.abspath(args.output)))
if(args.embed):
    im = Image.open(args.img)
    h, w = im.height, im.width
    ov = genpalette(w, h)
    ov.putalpha(170) #change overlay image alpha from 0-255
    #im.paste(ov, (0, h-40), mask=ov) #overlay as color stripe on bottom
    im.paste(ov, (0, 0), mask=ov) #overlay over entire image with transparency
    im.save(args.embed)
    print(str("Overlayed image saved at " + os.path.abspath(args.embed)))
