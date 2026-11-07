"""
COR3 Haus Production - GLS media pipeline.
Reads originals from ORIG (the untouched ZIP copy), writes optimised WebP images,
favicons, OG card and compressed videos into assets/. Re-runnable.
"""
import os, subprocess
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
ORIG = '/home/claude/gls_original/GLS/images'
OUT  = '/home/claude/gls/GLS/assets'
IMG  = os.path.join(OUT, 'img')

# (source file, output base name, widths, quality)
IMAGES = [
 ('16.png', 'condensing-unit-copper-receiver', (2000,1200,800), 80),
 ('15.png', 'brazing-compressor-connection',   (2000,1200,800), 80),
 ('AC.JPEG', 'compressor-rack-control-boxes',  (900,600), 70),
 ('AC3.jpeg','evaporator-coils-in-frame',      (900,600), 70),
 ('AC4.jpeg','rooftop-split-units-corrugated-roof',(1600,1000,640), 70),
 ('AC5.jpeg','ceiling-mounted-indoor-unit-pipework',(900,600), 70),
 ('AC6.jpeg','condenser-fan-assembly-guard',   (900,600), 70),
 ('FAN.jpeg','round-cassette-unit-fan-grille', (900,600), 70),
 ('FRIDGE.jpeg','condensing-unit-on-stand-r410a',(900,600), 70),
 ('FRIDGE1.jpeg','hermetic-compressor-wall-mounted',(1200,700), 70),
 ('FRIDGE2.jpeg','condensing-unit-rooftop-platform',(1200,700), 70),
 ('TECH.jpeg','refrigeration-control-enclosure',(900,600), 70),
 ('TECH1.jpeg','contactor-bank-digital-controller',(1200,700), 70),
 ('WhatsApp Image 2025-06-26 at 11.09.04.jpeg','outdoor-unit-panel-removed-control-boards',(960,600), 70),
 ('WhatsApp Image 2026-01-29 at 13.33.09.jpeg','technician-rooftop-compressor',(1200,800,500), 70),
 ('new1.jpeg','manifold-gauges-refrigerant-cylinder-ladder',(521,), 70),
 ('new2.jpeg','wall-mounted-split-outdoor-units',(780,500), 70),
 ('new3.jpeg','outdoor-electrical-enclosure',(900,600), 70),
 ('new4.jpeg','timer-and-contactor-box',(1000,640), 70),
 ('new5.jpeg','outdoor-units-bracketed-brick-wall',(900,600), 70),
 ('new6.jpeg','split-unit-components-staged-copper-coil',(900,600), 70),
 ('new7.jpeg','outdoor-unit-ground-mounted',(1200,700), 70),
 ('new8.jpeg','rooftop-condensing-units-weathered',(900,600), 70),
]
manifest = {}
for src, base, widths, q in IMAGES:
    if 400 not in widths:
        widths = tuple(sorted(set(widths) | {400}, reverse=True))   # small phones/gallery tiles
    im = Image.open(os.path.join(ORIG, src))
    if im.mode != 'RGB': im = im.convert('RGB')
    if src == 'new1.jpeg':   # original has black letterbox bars (rows 0-31 and 992-1040)
        im = im.crop((0, 34, im.width, 989))
    sizes = []
    for w in widths:
        if w > im.width: w = im.width
        h = round(im.height * w / im.width)
        im.resize((w, h), Image.LANCZOS).save(os.path.join(IMG, f'{base}-{w}.webp'), 'WEBP', quality=q, method=6)
        sizes.append((w, h))
    manifest[base] = sizes
    print(f'{base:48s}', sizes)

# ---- logo (transparent) cropped to artwork ----
logo = Image.open(os.path.join(ORIG, 'gls logo no background.png')).convert('RGBA')
logo = logo.crop(logo.split()[-1].getbbox())
for w in (480, 240, 120):
    logo.resize((w, round(logo.height * w / logo.width)), Image.LANCZOS).save(os.path.join(IMG, f'gls-logo-{w}.webp'), 'WEBP', quality=90, method=6)
logo.resize((480, round(logo.height*480/logo.width)), Image.LANCZOS).save(os.path.join(IMG, 'gls-logo-480.png'), optimize=True)
print('logo', logo.size)

# ---- favicons: logo on ink plate ----
INK = (21, 37, 47)
def plate(size, pad=0.14):
    p = Image.new('RGBA', (size, size), INK + (255,))
    inner = int(size * (1 - 2*pad))
    l = logo.copy(); l.thumbnail((inner, inner), Image.LANCZOS)
    p.alpha_composite(l, ((size - l.width)//2, (size - l.height)//2))
    return p
for n in (32, 180, 192, 512):
    plate(n).convert('RGB').save(os.path.join(OUT, '..', f'favicon-{n}.png' if n==32 else f'icon-{n}.png'), optimize=True)
plate(256).save(os.path.join(OUT, '..', 'favicon.ico'), sizes=[(16,16),(32,32),(48,48)])
os.replace(os.path.join(OUT,'..','icon-180.png'), os.path.join(OUT,'..','apple-touch-icon.png'))

# ---- Open Graph card 1200x630: ink plate with logo | photo ----
card = Image.new('RGB', (1200, 630), INK)
ph = Image.open(os.path.join(ORIG, '16.png')).convert('RGB')
tw, th = 760, 630
r = max(tw/ph.width, th/ph.height); ph = ph.resize((round(ph.width*r), round(ph.height*r)), Image.LANCZOS)
x0 = (ph.width - tw)//2; ph = ph.crop((x0, 0, x0+tw, th))
card.paste(ph, (440, 0))
l = logo.copy(); l.thumbnail((340, 340), Image.LANCZOS)
c = card.convert('RGBA'); c.alpha_composite(l, ((440-l.width)//2, (630-l.height)//2))
c.convert('RGB').save(os.path.join(IMG, 'og-gls-refrigeration-air-conditioning.jpg'), quality=84, optimize=True, progressive=True)

# ---- videos ----
VIDEOS = [
 ('WhatsApp Video 2025-06-26 at 11.10.05.mp4', 'outdoor-unit-control-boards'),
 ('WhatsApp Video 2026-01-29 at 13.33.10 (1).mp4', 'compressor-copper-rooftop'),
 ('WhatsApp Video 2026-01-29 at 13.33.10.mp4', 'rooftop-refrigerant-service'),
 ('WhatsApp Video 2026-01-29 at 14.13.49.mp4', 'rooftop-outdoor-units-team'),
]
for src, base in VIDEOS:
    out = os.path.join(OUT, 'video', base + '.mp4')
    if os.path.exists(out): continue   # videos were encoded once with crf 33 (see README)
    subprocess.run(['ffmpeg','-v','error','-y','-i',os.path.join(ORIG,src),
        '-vf',"scale='min(720,iw)':-2",'-c:v','libx264','-crf','28','-preset','slow','-pix_fmt','yuv420p',
        '-c:a','aac','-b:a','64k','-movflags','+faststart',out], check=True)
    subprocess.run(['ffmpeg','-v','error','-y','-ss','1','-i',os.path.join(ORIG,src),'-frames:v','1',
        '-vf',"scale='min(720,iw)':-2",os.path.join('/tmp', base+'.png')], check=True)
    Image.open(os.path.join('/tmp', base+'.png')).convert('RGB').save(os.path.join(IMG, f'poster-{base}.webp'),'WEBP',quality=74,method=6)
    d = Image.open(os.path.join(IMG, f'poster-{base}.webp'))
    print(base, d.size, os.path.getsize(out)//1024, 'KB video')
