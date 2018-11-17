import bpy

import os
import re

import subprocess

from datetime import datetime

from git import *

def write_obj(name, sha):
    repo = Repo(path = "./kit/" + name)
    
    commit = list(repo.iter_commits(repo.heads.master))
      
    entry = list(list(commit)[0].tree.traverse())[0]

    cont = repo.git.show('{}:{}'.format(sha, entry.path))
			
    f = open("./kit/tmp.obj", "w")
    f.write(cont)
    f.close()
    
class ChangeName(bpy.types.Operator):
    bl_label = "Change Name"
    bl_idname = "object.change_name"
    
    # name
    name = bpy.props.StringProperty(name = "name")
 
    def invoke(self, ctx, e):     
        return ctx.window_manager.invoke_props_dialog(self)

    def execute(self, ctx):
        global globalName
        globalName = self.name
        
        repo = Repo(path = "./kit/" + globalName)

        commit = repo.iter_commits(repo.heads.master)
        
        global globalShaList
        globalShaList = list(map(lambda _: str(_), list(commit)))
        
        return {"FINISHED"}
    
class ChangeSha(bpy.types.Operator):
    bl_label = "Change SHA"
    bl_idname = "object.change_sha"

    def invoke(self, ctx, e):
        return ctx.window_manager.invoke_props_dialog(self)

    def execute(self, ctx):
        global globalName
        print(globalName)
        """
            
        repo = Repo(path = "./kit/" + "asdf")

        commit = repo.iter_commits(repo.heads.master)
            
        sha = bpy.props.EnumProperty(items = list(map(lambda _: (str(_).upper(), str(_), ""), commit)))
        """
        return {"FINISHED"}
    
class Change(bpy.types.Operator):
    bl_label = "Reset"
    bl_idname = "object.change"

    def execute(self, ctx):
        print(globalShaList)
        
        write_obj(globalName, globalSha)
        
        if globalName in bpy.data.objects:
            bpy.data.objects[globalName].select = True 
            bpy.ops.object.delete()     
            
        bpy.ops.import_scene.obj(filepath = "./kit/tmp.obj") 
                    
        bpy.context.selected_objects[0].name = globalName
        
        return {"FINISHED"}

class Reset(bpy.types.Operator):
    bl_label = "Reset"
    bl_idname = "object.reset"
    
    name = bpy.props.StringProperty(name = "name")
    
    repo = Repo(path = "./kit/" + "asdf")

    commit = repo.iter_commits(repo.heads.master)
        
    sha = bpy.props.EnumProperty(items = list(map(lambda _: (str(_).upper(), str(_), ""), commit)))

    def invoke(self, ctx, e):
        return ctx.window_manager.invoke_props_dialog(self)

    def execute(self, ctx): 
        write_obj(self.name, self.sha)
        
        if self.name in bpy.data.objects:
            bpy.data.objects[self.name].select = True 
            bpy.ops.object.delete()     
            
        bpy.ops.import_scene.obj(filepath = "./kit/tmp.obj") 
                    
        bpy.context.selected_objects[0].name = self.name
        
        return {"FINISHED"} 
        
class Kit(bpy.types.Panel):  
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_label = "History"
    bl_context = "objectmode"
    bl_category = "Kit"
    
    def draw(self, ctx):
        self.layout.operator("object.change_name", text = "Change name")
        self.layout.operator("object.change_sha", text = "Change SHA")
        self.layout.operator("object.change", text = "Change")
    
        obj = [f for f in os.listdir("./kit") if os.path.isdir(os.path.join("./kit", f))]
       
        for _ in obj:
            # header
            self.layout.label(text = _)
            
            repo = Repo(path = "./kit/" + _)

            tree = repo.tree()
            for blob in tree:
                # tree
                for commit in list(repo.iter_commits(paths = blob.path)):
                    self.layout.label("\"" + commit.message + "\"")
                
                # timestamp
                unix_timestamp = commit.committed_date
                
                date = datetime.fromtimestamp(unix_timestamp)
                format = date.strftime("%d %b %Y %H:%M")
                
                self.layout.label(text = format)
           
            self.layout.separator()
           
            # change
            self.layout.operator("object.reset", text = "Update")
            
            self.layout.separator()

def register():
    bpy.utils.register_class(ChangeName)
    bpy.utils.register_class(ChangeSha)
    bpy.utils.register_class(Change)
    bpy.utils.register_class(Reset)
    bpy.utils.register_class(Kit)

def unregister():
    bpy.utils.unregister_class(ChangeName)
    bpy.utils.unregister_class(ChangeSha)
    bpy.utils.unregister_class(Change)
    bpy.utils.unregister_class(Reset)
    bpy.utils.unregister_class(Kit)
    
if __name__ == "__main__":
    register()
