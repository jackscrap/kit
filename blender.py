import bpy
from bpy.types import Panel

import os
import re

from datetime import datetime

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
        l = open(os.getcwd() + "/kit/test/.git/logs/refs/heads/master", "r").readlines()

        # SHA
        self.layout.prop(ctx.scene, "commit")

        # message
        msg = list(map(lambda _ : re.search("(?<=commit).+", _).group(0), l))

        self.layout.label(text = msg[0])

        # timestamp
        timestamp = re.search("(?<= )\d{10}(?= )", l[0]).group(0)

        date = datetime.fromtimestamp(int(timestamp))
        format = date.strftime('%d %b %Y %H:%M')

        self.layout.label(text = format)

        # branch
        # branch = os.listdir(os.getcwd() + "/kit/test/.git/refs/heads")

        """

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
    bpy.utils.unregister_class(Kit)

if __name__ == "__main__":
    register()
