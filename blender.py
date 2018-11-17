import bpy
from bpy.types import Panel

import os
import re

from datetime import datetime

bl_info = {
    "name": "Kit",
    "category": "Object"
}

# commit menu
"""
class Commit(bpy.types.Menu):
    bl_idname = "kit_commit"
    bl_label = "SHA"

    def draw(self, context):
        for asdf in ["asdf", "hjkl"]:
            self.layout.operator("object.select_all", text = asdf).action = "TOGGLE"
"""

# import
class Reset(bpy.types.Operator):
    bl_idname = "object.reset"
    bl_label = "Import Object"

    name = "test"

    if name in bpy.context.scene.objects:
        bpy.context.scene.objects[name].select = True

        bpy.ops.object.delete()

    bpy.ops.import_scene.obj(filepath = "./kit/" + name + "/" + "test" + ".obj")

    bpy.context.selected_objects[0].name = name

class Asdf(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_label = "asdf"
    bl_context = "objectmode"
    bl_category = "Kit"

    def draw(self, ctx):
        print("asdf")

class Kit(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_label = "test"
    bl_context = "objectmode"
    bl_category = "Kit"

    def draw(self, ctx):
        i = 1

        # obj
        obj = os.listdir(os.getcwd() + "/kit")

        for _ in obj:
            self.layout.operator("mesh.primitive_cube_add", _)

        ref = open(os.getcwd() + "/kit/test/.git/logs/refs/heads/master", "r").readlines()

        # SHA
        self.layout.prop(ctx.scene, "commit")

        # message
        msg = list(map(lambda _ : re.search("(?<=commit).+", _).group(0), ref))

        self.layout.label(text = msg[i])

        # time
        unix_timestamp = re.search("(?<= )\d{10}(?= )", ref[i]).group(0)

        date = datetime.fromtimestamp(int(unix_timestamp))
        format = date.strftime("%d %b %Y %H:%M")

        self.layout.label(text = format)

        # branch
        # branch = os.listdir(os.getcwd() + "/kit/test/.git/refs/heads")

        # change
        # property_1 = bpy.props.StringProperty()

        self.layout.operator("object.reset", text = "Update")

        """
        if not "asdf" in bpy.data.objects:
            bpy.ops.import_scene.obj(filepath="kit/test/test.obj")

            print(bpy.context.scene.objects.active.name)

        else:
            print("this it it chief")
        """

def register():
    bpy.utils.register_class(Reset)
    bpy.utils.register_class(Asdf)
    bpy.utils.register_class(Kit)

    # commit
    commit = open(os.getcwd() + "/kit/test/.git/logs/refs/heads/master", "r").readlines()

    sha = []
    msg = []
    for _ in commit:
        word = _.split(" ")

        fst = word[0]
        trunc = fst[0:5]
        sha.append(trunc)

        msg.append(re.search(r"(?<=commit).+", _).group(0))

    bpy.types.Scene.commit = bpy.props.EnumProperty(
        name = "Commit",
        items = list(map(lambda _: ("asdf".upper(), _, "asdf"), sha))
    )

def unregister():
    bpy.utils.register_class(Reset)
    bpy.utils.register_class(Asdf)
    bpy.utils.unregister_class(Kit)

if __name__ == "__main__":
    register()
