import bpy
import bmesh

scene = bpy.context.scene
src = bpy.data.objects['Plane']
frames = 100
col = bpy.data.collections.new(name="OUTPUT")
bpy.context.scene.collection.children.link(col)
imgName = "frames_" 
zeroPads = 4
for x in range(1,frames+1):
    
    newObj = src.copy()
    newObj.data = src.data.copy()
    newObj.animation_data_clear()
   
    col.objects.link(newObj)
    
    newObj.select_set(True)
    bpy.context.view_layer.objects.active = newObj
    
    box_material_obj = bpy.data.materials.new(str(x) + '_frame_mat')
    box_material_obj.use_nodes = True

    bsdf           = box_material_obj.node_tree.nodes["Principled BSDF"]
    texImage       = box_material_obj.node_tree.nodes.new('ShaderNodeTexImage')
    texImage.image = bpy.data.images.load( bpy.path.abspath("//"+imgName+str(x).zfill(4)+".png") )
    
    box_material_obj.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])
    #box_material_obj.node_tree.links.new(bsdf.inputs['Emissive'], texImage.outputs['Color'])
    newObj.data.materials.append(box_material_obj)
    
    bpy.context.scene.frame_set(x)

    newObj.scale = [0.001,0.001,0.001]
    newObj.keyframe_insert(data_path="scale", frame=x-1)
    newObj.keyframe_insert(data_path="scale", frame=x+1)
    
    newObj.scale = [1,1,1]
    newObj.keyframe_insert(data_path="scale", frame=x)
    
    fcurves = newObj.animation_data.action.fcurves
    for fcurve in fcurves:
        for kf in fcurve.keyframe_points:
            kf.interpolation = 'CONSTANT'



   