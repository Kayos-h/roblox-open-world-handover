local L = _G.L
local old = workspace:FindFirstChild('SpawnTown'); if old then old:Destroy() end
local test = L.folder(workspace, 'TEST_Builds')
local base = L.CF(0, 0, 0)
-- ground slab for test
L.part(test, L.V(200, 1, 120), L.CF(0, -0.5, 0), Color3.fromRGB(96,150,70), L.M.grass)
L.house(test, L.CF(-40, 0, 0), {w=26, d=20, floors=2, jetty=true, flowers=true, roof=L.C.roofRed, shutter=L.C.shutterGreen, stoneGround=true, name='TestHouseA'})
L.house(test, L.CF(10, 0, 0)*L.A(0, math.rad(20), 0), {w=20, d=16, floors=1, fh=12, roof=L.C.roofBlue, wall=L.C.plasterB, shutter=L.C.shutterBlue, name='TestCottage'})
L.house(test, L.CF(55, 0, -5), {w=22, d=26, floors=3, fh=10, jetty=true, ridgeZ=true, roof=L.C.roofBrown, wall=L.C.plasterC, shutter=L.C.shutterRed, name='TestTall'})
L.stall(test, L.CF(-10, 0, 35), Color3.fromRGB(180,50,50))
L.barrel(test, L.CF(20, 0, 30)); L.crate(test, L.CF(26, 0, 30)); L.haybale(test, L.CF(32, 0, 30)); L.haybale(test, L.CF(40, 0, 30), true)
L.lamp(test, L.V(-25, 0, 28)); L.bench(test, L.CF(0, 0, 45)); L.cart(test, L.CF(60, 0, 35), 'goods')
L.tree(test, L.V(-80, 0, 20), 1); L.tree(test, L.V(85, 0, 30), 1, 'pine'); L.bush(test, L.V(-60, 0, 30)); L.rock(test, L.V(-70, 0, -30), 1)
L.flowers(test, L.V(-45, 0, 25), 6, 30)
L.fence(test, L.V(-60, 0, 45), L.V(-20, 0, 45))
L.banner(test, L.CF(30, 14, 12)*L.A(0,0,0), Color3.fromRGB(70,40,120), 10, L.C.gold)
local cam = workspace.CurrentCamera
cam.CameraType = Enum.CameraType.Scriptable
cam.CFrame = L.CF(L.V(10, 45, 110), L.V(10, 12, 0))
local n = 0; for _, d in ipairs(test:GetDescendants()) do if d:IsA('BasePart') then n = n + 1 end end
return 'test built parts=' .. n
