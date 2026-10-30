-- sea_test: sets water properties from args and returns them. Args: {"r":8,"g":40,"b":76,"t":0.7,"refl":0.25}
local D = game:GetService('HttpService'):JSONDecode([==[__DATA__]==])
local T = workspace.Terrain
T.WaterColor = Color3.fromRGB(D.r, D.g, D.b)
T.WaterTransparency = D.t
T.WaterReflectance = D.refl
return string.format('water rgb(%d,%d,%d) t=%.2f refl=%.2f', D.r, D.g, D.b, D.t, D.refl)
