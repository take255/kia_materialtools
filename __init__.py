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


class KIAMATERIAL_Props_OA(PropertyGroup):
    material_color : FloatVectorProperty( name = "mycolor",subtype = "COLOR",size = 4, min=0.0, max=1.0, default=(0.75,0.0,0.8,1.0) )


#---------------------------------------------------------------------------------------
#Vertex Color List
#---------------------------------------------------------------------------------------

class VertexColorItem(bpy.types.PropertyGroup):
    color_value = bpy.props.FloatVectorProperty(
        name="Color", 
        subtype="COLOR", 
        min=0.0, 
        max=1.0,
        # get=get_color_value,
        # set=set_color_value
    )

class VertexColorlist(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        layout.label("", icon="COLOR")
        layout.prop(item, "name",  "")
        layout.prop(item, "color_enum", "")
        layout.prop(item, "color_value", "")

#---------------------------------------------------------------------------------------
#マテリアル関連ツール
#---------------------------------------------------------------------------------------
class KIATOOLS_MT_materialtools(Operator):
    bl_idname = "kiatools.materialtools"
    bl_label = "material"

    def execute(self, context):
        return{'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        props = bpy.context.scene.kiatools_oa
        layout=self.layout

        row = layout.row(align=False)
        col = row.column()

        box = col.box()
        box.label(text = 'vertex color')
        col = box.column()
        row = col.row()        
        row.prop(props, "material_type" )
        row.prop(props, "material_index" )

        row = col.row()
        row.operator("kiatools.material_assign_vertex_color", text = 'assign').mode = 0
        row.operator("kiatools.material_assign_vertex_color", text = 'assign(selected)').mode = 1
        row.operator("kiatools.material_convert_vertex_color")

        row = col.row()
        row.operator("kiatools.pick_vertex_color", text = 'pick').mode = True
        row.operator("kiatools.pick_vertex_color", text = 'put').mode = False

        box = col.box()
        box.label(text = 'vertex color')
        box.prop(props, "material_color")

        box.template_list(
            "SCENE_UL_my_color_list", 
            "my_color_list", 
            settings,
            "colors",
            settings,
            "active_color_index",
            type='DEFAULT'
        )