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

data = {}
obj = [f for f in os.listdir("./kit") if os.path.isdir(os.path.join("./kit", f))]
for name in obj:
    repo = Repo("./kit/" + name)

    sha = []
    for commit in repo.iter_commits(repo.heads.master):
        sha.append(commit.hexsha)

    data[name] = sha

class Kit(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_label = "History"
    bl_context = "objectmode"
    bl_category = "Kit"

    def draw(self, ctx):
        for _ in bpy.context.scene.commit:
            self.layout.label(text = _.name)

            self.layout.prop(
                ctx.scene.commit[_.name],
                "sha",
                text = "SHA"
            )

def reset(self, ctx):
    cont = repo.git.show("{}:{}".format(self.sha, "./" + self.name + ".obj"))

    f = open("./kit/tmp.obj", "w")
    f.write(cont)
    f.close()

    if self.name in bpy.data.objects:
        bpy.ops.object.delete()

    bpy.ops.import_scene.obj(filepath = "./kit/tmp.obj")

    bpy.context.scene.objects[0].name = self.name

def register():
    key = list(data.keys())[0]

    def func(self, ctx):
        return list(map(lambda _: (str(_)[:5], str(_)[:5], ""), data[key]))

    class Item(bpy.types.PropertyGroup):
        name = bpy.props.StringProperty()
        sha = bpy.props.EnumProperty(
            items = func,
            update = reset
        )

    bpy.utils.register_class(Item)

    bpy.types.Scene.commit = bpy.props.CollectionProperty(type = Item)

    bpy.context.scene.commit.clear()
    for obj in data:
        key = obj

        item = bpy.context.scene.commit.add()
        item.name = obj

    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
