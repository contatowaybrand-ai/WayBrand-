import numpy as np, sys
from PIL import Image, ImageFilter
fit=np.load('fit.npy'); mask=np.load('mask.npy')
Y0,Y1,X0,X1=40,385,55,935
soft=np.asarray(Image.fromarray((mask*255).astype('uint8')).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(3)))/255.
ov=np.asarray(Image.open(sys.argv[1])).astype(float); oa=ov[...,3:]/255; oc=ov[...,:3]
def comp(fr):
    f=fr.astype(float).copy(); R=f[Y0:Y1,X0:X1]
    f[Y0:Y1,X0:X1]=R*(1-soft[...,None])+fit*soft[...,None]
    return (f*(1-oa)+oc*oa).clip(0,255).astype('uint8')
if __name__=='__main__':
    src=np.asarray(Image.open(sys.argv[2])); out=comp(src); Image.fromarray(out).save(sys.argv[3])
