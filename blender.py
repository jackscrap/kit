import bpy
from bpy.types import Panel

import os
import re

# class for panel
class Kit(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_label = "History: "
    bl_context = "objectmode"
    bl_category = "Kit"

    def draw(self, ctx):
        layout = self.layout

        # obj
        f = os.listdir(os.getcwd() + "/test")

        regexObj = re.compile(".+\.obj")
        obj = list(filter(regexObj.match, f))

        """
        for f in obj:
            layout.operator("mesh.primitive_cube_add", text=f)
        """

        # branch
        branch = os.listdir(os.getcwd() + "/test/.git/refs/heads")

        # commit
        line = []
        commit = open(os.getcwd() + "/test/.git/logs/refs/heads/master", "r", encoding="utf-8")
        for c in commit:
            line.append(c)

        commit.close()

        for l in line:
            word = l.split(" ")

            fst = word[0]
            trunc = fst[0:5]

            msg = re.search(r"(?<=commit).+", l).group(0)
            print(msg)
            print("asdf")

            layout.operator("mesh.primitive_cube_add", text=trunc + " " + msg)

def register():
    bpy.utils.register_class(Kit)

def unregister():
    bpy.utils.unregister_class(Kit)

if __name__ == "__main__":
    register()
