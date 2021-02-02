from PIL import Image, ImageDraw, ImageFont
import os, sys

if(len(sys.argv) < 3):
    print("{} <image file> <number of colors in pallete [1-256]> <*palette output file>".format(sys.argv[0]))
    sys.exit(1)

END = "\x1b[0m"
def RGB(RGBl, Foreground=True):
    FB_G = 38
    if Foreground != True:
        FB_G = 48
    return "\x1b[" + str(FB_G) + ";2;" + str(RGBl[0]) + ";" + str(RGBl[1]) + ";" + str(RGBl[2]) + "m"

def rgbhex(rgb):
    return '%02x%02x%02x' % tuple(rgb)

def getpallete(f, num, v=True):
    img = Image.open(f)
    q = img.quantize(colors=num, method=2)
    paletteout = []
    for i in [j for j in range(num*3) if j%3==0]:
        c = q.getpalette()[i:i+3]
        paletteout.append(c)
        if(v):
            print(RGB(c), "■■■■■■■", END, str("#" + rgbhex(c)))
    return paletteout
numcol = int(sys.argv[2])

if(os.path.isfile(sys.argv[1])):
    pal = getpallete(sys.argv[1], numcol, v=True)
else:
    print("{} is not a valid file.".format(sys.argv[1]))
    sys.exit(1)

if(len(sys.argv) >= 4):
    w, h = 640, 360
    img = Image.new("RGB", (w, h))
    for i in range(numcol):
        dv = w/numcol
        shape = [(dv*i, 0), ((dv*i)+dv, h)]
        hx = "#" + rgbhex(pal[i])
        ImageDraw.Draw(img).rectangle(shape, fill=hx)

    img.save(sys.argv[3])
    print(str("Color palette saved at " + os.path.abspath(sys.argv[3])))
