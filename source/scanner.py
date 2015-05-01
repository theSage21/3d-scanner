import os
import pickle
from PIL import Image
from math import sin,cos,radians,pi

CAMERA_ANGLE=pi/6
CENTER=1920/2

def real_radius(x):
    global CENTER,CAMERA_ANGLE
    return (CENTER+x)/sin(CAMERA_ANGLE)
def get_slice_points(im):
    slice_pts=[]
    width,height=im.size
    for index,value in enumerate(im.getdata()):
        if value!=0:
            x,y=index%width,int(index/width)
            rad=real_radius(x)
            slice_pts.append(rad)
        else:
            slice_pts.append(0)#At center
    return slice_pts

def rad_to_3d(slices,rate,z_scale=0.1):
    """return a collection of points.
    rate is the angle between each slice"""
    scene=[]
    angle=0
    for sl in slices:
        for index,pt in enumerate(sl):
            x=pt*cos(angle)
            y=pt*sin(angle)
            z=index*z_scale
            scene.append((x,y,z))
    return tuple(scene)
def write_slice(sl,name):
    f=open('slices/'+name,'wb')
    pickle.dump(sl,f)
    f.close()
def reconstruct_from_images(pics):
    f=open('done','a')
    for pic in pics:
        im=Image.open(pic)
        sl=get_slice_points(im)
        write_slice(sl,pic.split('/')[-1].split('.')[0])
        #---
        print(pic,end='\r')
        f.write(pic+'\n')
    f.close()
    #----------
    slices=[]
    for i in (i.split('/')[-1].split('.')[0] for i in pics):
        f=open('slices/'+i,'rb')
        slices.append(pickle.load(f))
        f.close()
    #----------
    step=0.01
    rate=step
    while rate<5:
        print(rate)
        scene=rad_to_3d(slices,rate)
        f=open('scene_'+str(rate),'wb')
        pickle.dump(scene,f)
        f.close()
        rate+=step
def run():
    root=os.path.join(os.getcwd(),'clean_images')
    f=open('done','r')
    done=[i.strip() for i in f.readlines()]
    f.close()
    pics=[os.path.join(root,i) for i in sorted(os.listdir(root))]
    pics_to_do=[i for i in pics if i not in done]
    reconstruct_from_images(pics_to_do)
if __name__=='__main__':
    while True:
        try:run()
        except:pass
