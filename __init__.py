# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy
from bpy.types import ( PropertyGroup , Panel , Operator ,UIList)
import imp

from bpy.props import(
    PointerProperty,
    IntProperty,
    BoolProperty,
    StringProperty,
    CollectionProperty,
    FloatProperty,
    EnumProperty,
    FloatVectorProperty
    )

from . import utils
from . import cmd

imp.reload(utils)
imp.reload(cmd)

bl_info = {
"name": "kiamaterialtools",
"author": "kisekiakeshi",
"version": (0, 1),
"blender": (2, 80, 0),
"description": "kiamaterialtools",
"category": "Object"}

#MATERIAL_TYPE = ( ('METAL','METAL','') , ('LEATHER','LEATHER','') , ('CLOTH','CLOTH','') , ('OTHERS','OTHERS','') , ('BUFFER','BUFFER','') )

MATERIAL_TYPE = []
for vc in cmd.VERTEX_COLOR:
    MATERIAL_TYPE.append( (vc,vc,'') )

class KIAMATERIALTOOLS_Props_OA(PropertyGroup):
    material_color : FloatVectorProperty( name = "Select Face",subtype = "COLOR",size = 4, min=0.0, max=1.0, default=(0.75,0.0,0.8,1.0) )
    material_type : EnumProperty(items = MATERIAL_TYPE , name = 'type' ,update = cmd.change_mattype)
    material_index : IntProperty( name = "number", min=0, max=10, default=1 )



#---------------------------------------------------------------------------------------
#Vertex Color List
#---------------------------------------------------------------------------------------

class KIAMATERIALTOOLS_UL_uilist(UIList):
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:

            #item.nameが表示される
            #layout.prop(item, "bool_val", text = "")
            #layout.prop(item, "name", text="", emboss=False, icon_value=icon)
            layout.prop(item, "name", text="", emboss=False, icon_value=icon)
            layout.prop(item, "color",text= "")

        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)

#---------------------------------------------------------------------------------------
#マテリアル関連ツール
#---------------------------------------------------------------------------------------
class KIAMATERIALTOOLS_PT_materialtools(utils.panel):
    # bl_idname = "kiatools.materialtools"
    bl_label = "material tools"

    # def execute(self, context):
    #     #cmd.add(cmd.VERTEX_COLOR[0])

    #      return{'FINISHED'}

    def invoke(self, context, event):
        cmd.add(cmd.VERTEX_COLOR[0])
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        props = bpy.context.scene.kiamaterialtools_oa
        ui_list = context.window_manager.kiamaterialtools_list

        layout=self.layout

        row = layout.row(align=False)
        col = row.column()

        box = col.box()
        box.label(text = 'vertex color')

        col = box.column()
        row = col.row()        
        row.prop(props, "material_type" )
        #row.prop(props, "material_index" )

        col.template_list("KIAMATERIALTOOLS_UL_uilist", "", ui_list, "itemlist", ui_list, "active_index", rows=8)

        row = col.row()
        row.operator("kiamaterialtools.assign_vertex_color", text = 'assign').mode = 0
        row.operator("kiamaterialtools.assign_vertex_color", text = 'assign(selected)').mode = 1

        row = col.row()
        row.operator("kiamaterialtools.convert_vertex_color")



        box = col.box()
        #box.label(text = 'vertex color')
        box.prop(props, "material_color")

        row = box.row()
        row.operator("kiamaterialtools.pick_vertex_color", text = 'pick').mode = 2
        row.operator("kiamaterialtools.pick_vertex_color", text = 'assign').mode = 0
        row.operator("kiamaterialtools.pick_vertex_color", text = 'assign selected').mode = 1



        # box.template_list(
        #     "SCENE_UL_my_color_list", 
        #     "my_color_list", 
        #     settings,
        #     "colors",
        #     settings,
        #     "active_color_index",
        #     type='DEFAULT'
        # )
        


class KIAMATERIALTOOLS_Props_item(PropertyGroup):
    name : StringProperty(get=cmd.get_item, set=cmd.set_item)
    color : FloatVectorProperty(
        name = "color",subtype = "COLOR",size = 4, min=0.0, max=1.0,
        get=cmd.get_color_value,
        set=cmd.set_color_value
        )
    #bool_val : BoolProperty( update = cmd.showhide )

bpy.utils.register_class(KIAMATERIALTOOLS_Props_item)

#---------------------------------------------------------------------------------------
class KIAMATERIALTOOLS_Props_list(PropertyGroup):
    active_index : IntProperty()
    itemlist : CollectionProperty(type=KIAMATERIALTOOLS_Props_item)#アイテムプロパティの型を収めることができるリストを生成










#---------------------------------------------------------------------------------------
#マテリアルツール
#---------------------------------------------------------------------------------------
class KIAMATERIALTOOLS_OT_assign_vertex_color(Operator):
    bl_idname = "kiamaterialtools.assign_vertex_color"
    bl_label = "assign vtxcolor"
    mode : IntProperty()
    def execute(self, context):
        cmd.assign_vertex_color(self.mode)
        return {'FINISHED'}

class KIAMATERIALTOOLS_OT_convert_vertex_color(Operator):
    """シェーダーはPrincipled BSDFにすること"""
    bl_idname = "kiamaterialtools.convert_vertex_color"
    bl_label = "convert vtxcolor"
    def execute(self, context):
        cmd.convert_vertex_color()
        return {'FINISHED'}

class KIAMATERIALTOOLS_OT_pick_vertex_color(Operator):
    """ First, select polugon face (not vertex) and execute this command."""
    bl_idname = "kiamaterialtools.pick_vertex_color"
    bl_label = ""
    mode : IntProperty()
    def execute(self, context):
        cmd.pick_vertex_color(self.mode)
        return {'FINISHED'}






classes = (
    KIAMATERIALTOOLS_Props_OA,
    KIAMATERIALTOOLS_UL_uilist,
    KIAMATERIALTOOLS_Props_list,

    KIAMATERIALTOOLS_PT_materialtools,
    KIAMATERIALTOOLS_OT_assign_vertex_color,
    KIAMATERIALTOOLS_OT_convert_vertex_color,
    KIAMATERIALTOOLS_OT_pick_vertex_color
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.kiamaterialtools_oa = PointerProperty(type=KIAMATERIALTOOLS_Props_OA)
    bpy.types.WindowManager.kiamaterialtools_list = PointerProperty(type=KIAMATERIALTOOLS_Props_list)
    #cmd.add(cmd.VERTEX_COLOR[0])


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.kiamaterialtools_oa
    del bpy.types.WindowManager.kiamaterialtools_list
