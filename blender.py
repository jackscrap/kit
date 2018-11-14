import bpy
from bpy.types import Panel

import os
import re

# commit menu
"""
class Commit(bpy.types.Menu):
    bl_idname = "kit_commit"
    bl_label = "SHA"

    def draw(self, context):
        for asdf in ["asdf", "hjkl"]:
            self.layout.operator("object.select_all", text = asdf).action = "TOGGLE"
"""

class Kit(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_label = "test"
    bl_context = "objectmode"
    bl_category = "Kit"

    def draw(self, ctx):
        commit = open(os.getcwd() + "/kit/test/.git/logs/refs/heads/master", "r", encoding="utf-8")
        l = []
        for _ in commit:
            l.append(_)

        commit.close()

        msg = []
        for _ in l:
            msg.append(re.search(r"(?<=commit).+", _).group(0))\


        self.layout.prop(ctx.scene, "commit")

        # message
        self.layout.label(text = msg[0])


        """
        # branch
        branch = os.listdir(os.getcwd() + "/kit/test/.git/refs/heads")

        # commit
        self.layout.menu("kit_commit")

        line = []
        commit = open(os.getcwd() + "/kit/test/.git/logs/refs/heads/master", "r", encoding="utf-8")
        for c in commit:
            line.append(c)

        commit.close()

        for l in line:
            word = l.split(" ")

            fst = word[0]
            trunc = fst[0:5]

            msg = re.search(r"(?<=commit).+", l).group(0)

            self.layout.label(text = trunc + " " + msg)

        # change
        if not "asdf" in bpy.data.objects:
            bpy.ops.import_scene.obj(filepath="./test/test.obj")

            print(bpy.context.scene.objects.active.name)

        else:
            print("this it it chief")
        """


def register():
    bpy.utils.register_class(Kit)

    # commit
    commit = open(os.getcwd() + "/kit/test/.git/logs/refs/heads/master", "r", encoding="utf-8")
    l = []
    for _ in commit:
        l.append(_)

    commit.close()

    sha = []
    msg = []
    for _ in l:
        word = _.split(" ")

        fst = word[0]
        trunc = fst[0:5]

        sha.append(trunc)
        msg.append(re.search(r"(?<=commit).+", _).group(0))

    tup = []
    for _ in sha:
        tup.append(("asdf", _, "asdf"))

    bpy.types.Scene.commit = bpy.props.EnumProperty(
        name = "Commit",
        items = tup
    )

def unregister():
    #bpy.utils.unregister_claKitKit)
    bpy.utils.unregister_class(Kit)
    #bpy.utils.unregister_class(Commit)

if __name__ == "__main__":
    register()
