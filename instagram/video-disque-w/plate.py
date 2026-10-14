import numpy as np
from PIL import Image, ImageFilter
fr=np.stack([np.asarray(Image.open(f'all/{i:03d}.png')).astype(float) for i in range(1,361,4)])
med=np.median(fr,0)
Y0,Y1,X0,X1=40,385,55,935
R=med[Y0:Y1,X0:X1]
bg=np.array([229,236,234.])
diff=np.abs(R-R.reshape(-1,3).mean(0)).sum(-1)
txt=(R.sum(-1)<600)|((R[...,1]-R[...,0])>25)
m=Image.fromarray((txt*255).astype('uint8')).filter(ImageFilter.MaxFilter(9))
mask=np.asarray(m)>0
yy,xx=np.mgrid[Y0:Y1,X0:X1]
ok=~mask
# exclude arm (dark, right-bottom)
ok&=~((xx>850)&(yy>300))
def basis(y,x):
    y=(y-200)/200; x=(x-500)/500; return np.stack([np.ones_like(x),x,y,x*x,x*y,y*y,x**3,x*x*y,x*y*y,y**3],-1)
A=basis(yy[ok],xx[ok]); fit=np.zeros_like(R)
for c in range(3):
    co,*_=np.linalg.lstsq(A,R[...,c][ok],rcond=None); fit[...,c]=basis(yy,xx)@co
res=np.abs(R-fit)[ok]; print('residual mean',res.mean(),'p99',np.percentile(res,99))
np.save('fit.npy',fit); np.save('mask.npy',mask); np.save('med.npy',med)
