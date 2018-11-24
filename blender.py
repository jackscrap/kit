bl_info = {
    "name:": "Kit",
    "description": "Version control for Blender",
    "author": "jackhasakeyboard",
    "version": (0, 1),
    "category": "Object"
}

import bpy

from git import *

import os

obj = [f for f in os.listdir("./kit") if os.path.isdir(os.path.join("./kit", f))]

name = "asdf"
sha = []
repo = Repo("./kit/" + name)

for commit in repo.iter_commits(repo.heads.master):
  sha.append(commit.hexsha)

class Kit(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_label = "History"
    bl_context = "objectmode"
    bl_category = "Kit"

    def draw(self, ctx):
        # self.layout.operatr(

        for i, _ in enumerate(obj):
            box = self.layout.box()

            box.label(text = _)

            box.prop(ctx.scene, "sha", text = "SHA")

def reset(self, ctx):
    cont = repo.git.show("{}:{}".format(self.sha, "./" + name + ".obj"))

    f = open("./kit/tmp.obj", "w")
    f.write(cont)
    f.close()

    if name in bpy.data.objects:
        bpy.ops.object.delete()

    bpy.ops.import_scene.obj(filepath = "./kit/tmp.obj")

    bpy.context.scene.objects[0].name = name

    """
    bpy.types.Scene.asdf = bpy.props.StringProperty(name = "lol")
    print(bpy.types.Scene.asdf)
    """

def register():
    bpy.types.Scene.sha = bpy.props.EnumProperty(
        items = list(map(lambda _: (str(_), str(_)[:5], ""), sha)),
        update = reset
    )

    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
