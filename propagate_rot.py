
# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Propagate Rotation",
    "author": "Rev",
    "version": (1, 0),
    "blender": (3, 1, 0),
    "location": "",
    "description": "Copies local quaternion rotations of selected bones and propagates across selected keyframes. Requires the Free IK add-on in quaternion mode to work.",
    "warning": "",
    "doc_url": "",
    "category": "Animation"
}

import bpy

def propagaterot(context):
    scn = bpy.context.scene
    obj = bpy.context.object
    pose = obj.pose
    action = obj.animation_data.action

    bones = bpy.context.selected_pose_bones
    bones_checked = []

    for g in action.groups:
        if g.name not in bones_checked:
            for b in bones:
                if g.name == b.name:
                    bones_checked.append(g.name)
                    rot = b.free_ik_local_quaternion
                    
                    #print(g.name + b.name)
                    selected = False
                    for channel in g.channels :   # channel is fcurves
                        if selected:
                            break
                        #print(channel)
                        #print("  %s[%s] :"%(g.name,channel.array_index))
                        
                        for p in channel.keyframe_points :
                            #print("    is selected at frame %d %s"%(p.co[0], p.select_control_point ))
                            if p.select_control_point:
                                key = int(p.co[0])
                                
                                b.keyframe_insert('free_ik_local_quaternion', frame=key)
                                
                                #print(str(key) + " " + str(rot))
                                
                            selected = True


class PropagateRot(bpy.types.Operator):
    """Copies local quaternion rotations of selected bones and propagates across selected keyframes. Requires the Free IK add-on in quaternion mode to work"""
    bl_idname = "pose.propagaterot"
    bl_label = "Propagate Rotation"

    def execute(self, context):
        propagaterot(context)
        return {'FINISHED'}


def menu_func(self, context):
        self.layout.operator(PropagateRot.bl_idname, text=PropagateRot.bl_label)
        
# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access)
def register():
    bpy.utils.register_class(PropagateRot)
    bpy.types.VIEW3D_MT_pose.append(menu_func)


def unregister():
    bpy.utils.unregister_class(PropagateRot)
    bpy.types.VIEW3D_MT_pose.remove(menu_func)


if __name__ == "__main__":
    register()

    # test call
    #bpy.ops.object.simple_operator()
