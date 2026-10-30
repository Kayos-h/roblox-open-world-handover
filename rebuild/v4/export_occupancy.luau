-- Exports footprints of existing placed models for one Phase1Map area (or SpawnTown / Enterable). Args JSON: {"area":"v3_capital"}
-- Returns [[x,z,hx,hz],...] with axis-aligned half extents rounded to 0.1.
local D = game:GetService("HttpService"):JSONDecode([==[__DATA__]==])
local root = D.area == "SpawnTown" and workspace:FindFirstChild("SpawnTown") or (workspace:FindFirstChild("Phase1Map") and workspace.Phase1Map:FindFirstChild(D.area))
if not root then return "[]" end
local out = {}
local n = 0
local function add(cf, size)
  local r = cf.RightVector
  local u = cf.LookVector
  local hx = (math.abs(r.X) * size.X + math.abs(u.X) * size.Z) / 2
  local hz = (math.abs(r.Z) * size.X + math.abs(u.Z) * size.Z) / 2
  out[#out + 1] = { math.floor(cf.X * 10 + 0.5) / 10, math.floor(cf.Z * 10 + 0.5) / 10, math.floor(hx * 10 + 0.5) / 10, math.floor(hz * 10 + 0.5) / 10 }
end
for _, d in ipairs(root:GetDescendants()) do
  if d:IsA("Model") and (d:GetAttribute("PlanKey") or d.Parent == root or (d.Parent and d.Parent.Parent == root)) and not d:FindFirstAncestorWhichIsA("Model") then
    local ok, cf, size = pcall(function() return d:GetBoundingBox() end)
    if ok then add(cf, size) end
  elseif d:IsA("Model") and d:GetAttribute("PlanKey") then
    local ok, cf, size = pcall(function() return d:GetBoundingBox() end)
    if ok then add(cf, size) end
  elseif d:IsA("BasePart") and not d:FindFirstAncestorWhichIsA("Model") then
    add(d.CFrame, d.Size)
  end
  n += 1
  if n % 400 == 0 then task.wait() end
end
return game:GetService("HttpService"):JSONEncode(out)
