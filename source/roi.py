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
def clean_images(pics,raw_path,process_path):
    total_length=len(pics)
    for index,pic in enumerate(pics):
        im=Image.open(os.path.join(raw_path,pic))
        im=process(im)
        im.save(os.path.join(process_path,pic))

if __name__=='__main__':
    raw_path=os.path.join(os.getcwd(),'processed_images')
    process_path=os.path.join(os.getcwd(),'clean_images')
    print(raw_path)
    print(process_path)
    pics=os.listdir(raw_path)
    done=os.listdir(process_path)
    pics.sort()
    pic=[i for i in pics if i not in done]
    size=int(len(pic)/4)
    print(size)
    for i in range(4):
        job=pic[:size]
        pic=pic[size:]
        pid=os.fork()
        if pid==0:
            clean_images(pic,raw_path,process_path)
        else:print(pid)
