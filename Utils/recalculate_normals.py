import bpy
import os

# All object manipulation in scene is based on selection!!!!

path_to_obj_dir = '../Objects/test_normal/'
result_path_dir = '../Objects/recalculated_normals/'

# path = '/home/hyzi/Documents/test_normal/000026.obj'
# imported_obj = bpy.ops.import_scene.obj(filepath=path)



file_list = sorted(os.listdir(path_to_obj_dir))

obj_list = [item for item in file_list if item[-3:] == 'obj']

for x in obj_list:
    path_to_file = os.path.join(path_to_obj_dir, x)
    bpy.ops.import_scene.obj(filepath=path_to_file)

    scene = bpy.context.scene

    # start with empty selection
    bpy.ops.object.select_all(action='DESELECT')

    # loop through all objects in the scene
    for ob in scene.objects:

        # select this object
        scene.objects.active = ob
        ob.select = True

        # if this object is a mesh
        if ob.type == 'MESH':
            if ob.name != 'Cube' and ob.name != 'Lamp' and ob.name != 'Camera':
                # export to OBJ
                bpy.ops.export_scene.obj(filepath=result_path_dir + 'new_' + ob.name + '.obj', use_selection=True, use_normals=True, use_materials=False)
                bpy.ops.object.delete()
        # Not neccessary
        bpy.data.scenes.remove(scene, True)
        # deselect this object again
        ob.select = False
