import os
import pickle
from PIL import Image
from math import sin,cos,radians,pi

CAMERA_ANGLE=pi/6
CENTER=1920/2

def real_radius(x):
    global CENTER,CAMERA_ANGLE
    return (x-CENTER)/sin(CAMERA_ANGLE)

def get_slice_points(im):
    slice_pts=[]
    width,height=im.size
    for index,value in enumerate(im.getdata()):
        if value!=0:
            x,y=index%width,int(index/width)
            rad=real_radius(x)
            slice_pts.append(rad)
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
        angle+=rate
    return tuple(scene)
def write_slice(sl,name):
    """Writes slice to file"""
    f=open('slices/'+name,'wb')
    pickle.dump(sl,f)
    f.close()
def reconstruct_from_images(pics):
    """Reconstruct from a sequence of images"""
    print('Generating slices form pictures')
    for pic in pics:
        try:
            im=Image.open(pic)
            sl=get_slice_points(im)
            write_slice(sl,pic.split('/')[-1].split('.')[0])
            #---
            print(pic,end='\r')
        except: print(pic)
    #----------
    print(' '*100,'\r','Gathering slices')
    slices=[]
    for i in sorted(os.listdir('slices')):
        f=open('slices/'+i,'rb')
        slices.append(pickle.load(f))
        f.close()
        print(i,end='\r')
    #----------
    print('Generating scene from slices')
    step=0.1
    rate=2*pi/len(slices)
    while rate<195:
        scene=rad_to_3d(slices,rate)
        f=open('scenes/scene_'+str(rate),'wb')
        pickle.dump(scene,f)
        f.close()
        rate+=step
        break
def run():
    root=os.path.join(os.getcwd(),'clean_images')
    done=os.listdir(os.path.join(os.getcwd(),'slices'))
    pics=[os.path.join(root,i) for i in sorted(os.listdir(root)) if i.split('.')[0] not in done]
    reconstruct_from_images(pics)
if __name__=='__main__':
    run()
