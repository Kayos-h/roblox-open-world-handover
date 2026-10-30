local cam = workspace.CurrentCamera
cam.CameraType = Enum.CameraType.Scriptable
local args = {...}
cam.CFrame = CFrame.new(Vector3.new(-230,50,-420), Vector3.new(0,70,-575))
return 'cam ok'

