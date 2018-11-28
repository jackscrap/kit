bl_info = {
    "name": "Kit",
    "description": "Version control for Blender",
    "author": "jackhasakeyboard",
    "version": (0, 1),
    "category": "Object"
}

import bpy

from git import *

import os
from datetime import datetime

path = "/home/jack/.config/blender/2.79/scripts/addons/kit/obj/"

data = {}
obj = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
for name in obj:
    repo = Repo(path + name)

    sha = []
    for commit in repo.iter_commits(repo.heads.master):
        sha.append(commit.hexsha)

    data[name] = sha

class Set(bpy.types.Operator):
    bl_idname = "object.set"
    bl_label = "set"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene

        bpy.context.scene.commit.clear()
        for obj in data:
            key = obj

            item = bpy.context.scene.commit.add()
            item.name = obj

        return {"FINISHED"}

class Kit(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_label = "History"
    bl_context = "objectmode"
    bl_category = "Kit"

    def draw(self, ctx):
        self.layout.operator("object.set")

        for _ in bpy.context.scene.commit:
            cont = self.layout.box()

            cont.label(text = _.name)

            cont.prop(
                ctx.scene.commit[_.name],
                "sha",
                text = "SHA"
            )

            col = cont.column()
            for commit in repo.iter_commits(repo.heads.master):
                sub = col.box()

                sub.label(text = commit.hexsha[:5])

                sub.label(text = "\"" + commit.message.rstrip("\n") + "\"")

                val = datetime.fromtimestamp(commit.committed_date)
                format = val.strftime("%b %d %Y %H:%M")

                sub.label(text = format)

def reset(self, ctx):
    cont = repo.git.show("{}:{}".format(self.sha, "./" + self.name + ".obj"))

    f = open(path + "tmp.obj", "w")
    f.write(cont)
    f.close()

    if self.name in bpy.data.objects:
        bpy.ops.object.delete()

    bpy.ops.import_scene.obj(filepath = path + "tmp.obj")

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

    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
