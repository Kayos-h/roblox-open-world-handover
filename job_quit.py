import bpy
def _q():
    bpy.ops.wm.quit_blender()
    return None
bpy.app.timers.register(_q, first_interval=1.0)
print('quit scheduled')
