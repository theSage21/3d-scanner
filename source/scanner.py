import os
import pickle
from PIL import Image
from math import sin,cos,radians,pi

ANGLE_ROTATED=radians(68)#for room scan
#ANGLE_ROTATED=radians(360)#for the object scan
CAMERA_ANGLE=pi/6
CENTER=1920/2
DIST_FROM_LASER=CENTER/sin(CAMERA_ANGLE)

def real_radius(x):
    """Calculate displacement from axis of rotation along laser
    based on position in camera image"""
    global CENTER,CAMERA_ANGLE
    return (x-CENTER)/sin(CAMERA_ANGLE)

def get_slice_points(im):
    """Find brightest point in every row in the image and get the real
    radius for that image. Return a list of such points"""
    slice_pts=[]
    width,height=im.size
    last_y,max_val,max_index=0,0,0
    brightest=max(im.getdata())
    for index,value in enumerate(im.getdata()):
        x,y=index%width,int(index/width)
        if last_y!=y:#row has changed. append brightest point
            mx=max_index%width
            max_index=index
            max_val=value
            rad=real_radius(mx)
            slice_pts.append(rad)
        if value>=max_val:
            max_val=value
            max_index=index
        last_y=y
    return slice_pts

def rad_to_3d(slices,rate,rotating_cam,z_scale=0.1):
    """return a collection of points.
    rate is the angle between each slice"""
    scene=[]
    angle=0
    global DIST_FROM_LASER
    for sl in slices:
        for index,pt in enumerate(sl):
            if rotating_cam:
                pt=DIST_FROM_LASER-pt
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
def reconstruct_from_images(pics,rotating_cam=False):
    """Reconstruct from a sequence of images"""
    global ANGLE_ROTATED
    print('Generating slices from pictures')
    for pic in pics:
        try:
            im=Image.open(pic)
            im=im.convert('L')
            sl=get_slice_points(im)
            write_slice(sl,pic.split('/')[-1].split('.')[0])
            #---
            print(pic,end='\r')
        except Exception as e:
            print('-'*10)
            print(e)
            print(pic)
            print('-'*10)
    #----------
    print(' '*100,'\r','Gathering slices from disk')
    slices=[]
    for i in sorted(os.listdir('slices')):
        f=open('slices/'+i,'rb')
        sl=pickle.load(f)
        slices.append(sl)
        f.close()
        print(i,end='\r')
    #----------
    print('Generating scene from slices gathered')
    rate=ANGLE_ROTATED/len(slices)
    scene=rad_to_3d(slices,rate,rotating_cam)
    #-----save scene to file
    f=open('scene','wb')
    pickle.dump(scene,f)
    f.close()
def run(rotating_camera=False):
    root=os.path.join(os.getcwd(),'processed_images')
    if not os.path.exists('slices'):os.mkdir('slices')
    done=os.listdir(os.path.join(os.getcwd(),'slices'))
    pics=[os.path.join(root,i) for i in sorted(os.listdir(root)) if i.split('.')[0] not in done]
    #----------reconstruct
    reconstruct_from_images(pics,rotating_camera)

if __name__=='__main__':
    import sys
    if '-rotcam' in sys.argv:
        print('Rotating camera found to be True')
        run(True)
    else:run()
