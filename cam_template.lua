local cam = workspace.CurrentCamera
cam.CameraType = Enum.CameraType.Scriptable
local args = {...}
cam.CFrame = CFrame.new(Vector3.new(CAMX), Vector3.new(LOOKX))
return 'cam ok'
