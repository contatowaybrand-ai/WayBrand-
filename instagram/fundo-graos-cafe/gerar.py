# Recorta os grãos isolados da foto de referência e preenche um fundo 1080x1350 só de grãos.
import random, numpy as np
from PIL import Image, ImageFilter, ImageEnhance
from scipy import ndimage as nd
SRC='referencia.png'; OUT='fundo-graos-cafe-1080x1350.png'; W,H=1080,1350
random.seed(7)
im=Image.open(SRC).convert('RGB'); a=np.asarray(im).astype(int); r,g,b=a[...,0],a[...,1],a[...,2]
mask=(((r+g+b)/3)<215)&((r-b)>18); mask=nd.binary_opening(mask,iterations=1); mask=nd.binary_fill_holes(mask)
lab,n=nd.label(mask); beans=[]
for i,sl in enumerate(nd.find_objects(lab)):
    m=(lab[sl]==i+1); s=m.sum(); h,w=m.shape
    if not(60<s<400 and .4<h/w<2.5 and max(h,w)<30): continue
    px=a[sl][m]; lum=px.mean()
    fill=s/(h*w)
    if lum>95 or fill>.85: continue   # descarta pedaços claros/retangulares da embalagem
    pad=2; y0,y1=max(sl[0].start-pad,0),sl[0].stop+pad; x0,x1=max(sl[1].start-pad,0),sl[1].stop+pad
    crop=im.crop((x0,y0,x1,y1)); mm=np.zeros((y1-y0,x1-x0),bool); mm[sl[0].start-y0:sl[0].stop-y0, sl[1].start-x0:sl[1].stop-x0]=m
    mm=nd.binary_erosion(mm,iterations=1)          # tira a franja branca
    alpha=Image.fromarray((mm*255).astype('uint8'))
    k=6  # upscale
    big=crop.resize((crop.width*k,crop.height*k),Image.LANCZOS)
    big=big.filter(ImageFilter.UnsharpMask(radius=3,percent=120,threshold=2))
    big=ImageEnhance.Contrast(big).enhance(1.08)
    al=alpha.filter(ImageFilter.GaussianBlur(.8)).resize(big.size,Image.BICUBIC).filter(ImageFilter.GaussianBlur(3)).point(lambda v:0 if v<110 else (255 if v>150 else int((v-110)*255/40)))
    t=big.convert('RGBA'); t.putalpha(al); beans.append(t)
print(len(beans),'grãos')
canvas=Image.new('RGBA',(W,H),(38,22,14,255))
shadow_cache={}
def place(n,scale_rng):
    for _ in range(n):
        bn=random.choice(beans); s=random.uniform(*scale_rng)
        t=bn.resize((int(bn.width*s),int(bn.height*s)),Image.LANCZOS).rotate(random.uniform(0,360),expand=True,resample=Image.BICUBIC)
        if random.random()<.5: t=t.transpose(Image.FLIP_LEFT_RIGHT)
        x=random.randint(-t.width//2,W-t.width//2); y=random.randint(-t.height//2,H-t.height//2)
        sh=Image.new('RGBA',t.size,(0,0,0,0)); sh.putalpha(t.split()[3].point(lambda v:int(v*.55)).filter(ImageFilter.GaussianBlur(6)))
        canvas.alpha_composite(sh,(x+6,y+8)); canvas.alpha_composite(t,(x,y))
place(900,(0.8,1.0)); place(700,(0.9,1.1)); place(500,(1.0,1.15))
out=canvas.convert('RGB')
out=ImageEnhance.Color(out).enhance(1.05)
out.save(OUT,quality=95); print(OUT)
