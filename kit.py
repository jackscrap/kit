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

path = os.path.join(bpy.utils.script_path_user(), "addons/kit/obj")
 
data = {}
obj = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
for name in obj:
    repo = Repo(os.path.join(path, name))

    sha = []
    for commit in repo.iter_commits(repo.heads.master):
        sha.append(commit.hexsha)

    data[name] = sha

class Set(bpy.types.Operator):
    bl_idname = "object.set"
    bl_label = "set"

    def execute(self, ctx):
        bpy.context.scene.commit.clear()
        for obj in data:
            item = bpy.context.scene.commit.add()
            item.name = obj

        return {"FINISHED"}

class Kit(bpy.types.Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_label = "Kit"

    def draw(self, ctx):
        self.layout.operator("object.set")

        for _ in ctx.scene.commit:
            cont = self.layout.box()

            cont.label(text = _.name)
            
            cont.prop(
                ctx.scene.commit[_.name],
                "sha",
                text = "SHA"
            )

            repo = Repo(os.path.join(path, _.name))

            for _ in repo.iter_commits(repo.heads.master):
                sub = cont.box()

                # SHA
                sub.label(text = _.hexsha)

                # message
                sub.label(text = "\"" + _.message.rstrip("\n") + "\"")

                # date
                epoch = _.committed_date
                time = datetime.fromtimestamp(epoch)
                hrf = time.strftime("%d %b %Y %H:%M")
                sub.label(text = hrf)

def reset(self, ctx):
    repo = Repo(os.path.join(path, self.name))

    cont = repo.git.show(
        "{}:{}".format(
            self.sha,
            self.name + ".obj"
        )
    )

    f = open(os.path.join(path, "tmp.obj"), "w")
    f.write(cont)
    f.close()

    if self.name in bpy.data.objects:
        bpy.ops.object.delete()

    bpy.ops.import_scene.obj(filepath = os.path.join(path, "tmp.obj"))

    bpy.context.scene.objects[0].name = self.name

def func(self, ctx):
    return list(map(lambda _: (str(_), str(_)[:5], ""), data[self.name]))

def register():
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
