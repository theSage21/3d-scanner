SCANNER
=======

Takes a series of line scanned images and converts to a dot cloud 3D representation of an object.
We assume that the images are provided in chronological order and that rotation is constant.

The cloud generated may be a little off.

useage
------

1. get the video. Make sure everything is nice and dark except the laser.
2. convert the video to greyscale and save as series of images.(I use blender for this)
3. save the images to a folder called processed_images
4. Run roi.py In case it kills your pc run it again.
5. after roi.py has finished running run scanner.py
6. The file in the scenes folder is the generated object. It is a collection of (x,y,z) points
7. To plot the object you can use anything. I use blender.

Feel free to contact for any help. arjoonn(dot)94(at)gmail(dot)com

