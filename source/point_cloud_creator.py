import bpy
import os
import pickle

def open_scene(name):
    f=open(name,'rb')
    data=pickle.load(f)
    f.close()
    return data
def generate_point_cloud(context,vertices,name):
    mesh=bpy.data.meshes.new(name)
    mesh.from_pydata(vertices,[],[])
    mesh.update()
    from bpy_extras import object_utils
    return object_utils.object_data_add(context,mesh,operator=None)

def generate_scenes(scene_list):
    for data in scene_list:
        mesh=generate_point_cloud(bpy.context,data,scene)

data=open_scene('data')
mesh=generate_point_cloud(bpy.context,data,'scene')
