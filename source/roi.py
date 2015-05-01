from PIL import Image
import os

def process(im):
    "Find brightest in each row"
    width,height=im.size
    last_y=0
    max_val,max_index=0,0
    new_data=[]
    brightest=max(im.getdata())
    for index,value in enumerate(im.getdata()):
        x,y=index%width,int(index/width)
        #if the row has changed:
        if last_y!=y:
            new_data[max_index]=brightest
            max_index=index
            max_val=value
        #if a new max is found
        if value>=max_val:
            max_val=value
            max_index=index
        #---routine
        last_y=y
        new_data.append(0)
    im.putdata(new_data)
    return im
def clean_images():
    raw_path=os.path.join(os.getcwd(),'processed_images')
    process_path=os.path.join(os.getcwd(),'clean_images')
    pics=os.listdir(raw_path)
    pics.sort()
    total_length=len(pics)
    for index,pic in enumerate(pics):
        im=Image.open(os.path.join(raw_path,pic))
        im=process(im)
        im.save(os.path.join(process_path,pic))
        print(index/total_length,'% ',pic,end='\r')
if __name__=='__main__':
    clean_images()
