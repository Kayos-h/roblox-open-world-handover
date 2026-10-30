-- enterable footprints: bounding boxes of everything under Phase1Map.Enterable (any depth, top-most models) -> JSON [[x,z,hx,hz,name]]
local root = workspace.Phase1Map:FindFirstChild('Enterable')
local out = {}
if root then
  local function walk(inst)
    for _, c in ipairs(inst:GetChildren()) do
      if c:IsA('Model') then
        local cf, size = c:GetBoundingBox()
        if size.X > 4 then out[#out + 1] = { math.floor(cf.X + 0.5), math.floor(cf.Z + 0.5), math.floor(size.X / 2 + 0.5), math.floor(size.Z / 2 + 0.5), c.Name } end
      elseif c:IsA('Folder') then walk(c) end
    end
  end
  walk(root)
end
return game:GetService('HttpService'):JSONEncode(out)
