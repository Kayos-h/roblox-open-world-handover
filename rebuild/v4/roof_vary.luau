-- roof_vary: capital house roofs get varied hues. Models C05..C20 (not walls, not castle). Idempotent through the attribute RoofVaried2.
local cap = workspace.Phase1Map.v3_capital
local V = {
  { 'slate',   Color3.fromRGB(98, 104, 114) }, { 'brown',  Color3.fromRGB(126, 92, 66) },  { 'teal',   Color3.fromRGB(66, 118, 112) },
  { 'terra',   Color3.fromRGB(178, 98, 64) },  { 'olive',  Color3.fromRGB(108, 120, 86) }, { 'ochre',  Color3.fromRGB(186, 148, 88) },
  { 'navy',    Color3.fromRGB(70, 86, 120) },  { 'plum',   Color3.fromRGB(112, 74, 92) },  { 'sage',   Color3.fromRGB(122, 140, 112) },
}
local RED = { Color3.fromRGB(150, 64, 48), Color3.fromRGB(170, 84, 56), Color3.fromRGB(128, 70, 54), Color3.fromRGB(140, 104, 72) }
local nm, np = 0, 0
for _, g in ipairs(cap:GetChildren()) do
  if g.Name ~= 'Walls' and g.Name ~= 'Gardens' and g.Name ~= 'Lamps' and g.Name ~= 'Castle' and g.Name ~= 'CastleCourt' and g.Name ~= 'RoyalGarden' then
    for _, m in ipairs(g:GetChildren()) do
      if m:IsA('Model') and string.match(m.Name, '^C%d%d_') and not m:GetAttribute('RoofVaried2') then
        local pos = m:GetPivot().Position
        local seed = math.abs(math.floor(pos.X * 13 + pos.Z * 7))
        local v = V[(seed % #V) + 1][2]
        local r = RED[(seed % #RED) + 1]
        local touched = false
        for _, p in ipairs(m:GetChildren()) do
          if p:IsA('BasePart') then
            local n = p.Name
            if n == 'tile_a' then p.Color = v; touched = true; np += 1
            elseif n == 'tile_b' then p.Color = v:Lerp(Color3.new(0, 0, 0), 0.14); touched = true; np += 1
            elseif n == 'tile_grey' then p.Color = v:Lerp(Color3.fromRGB(110, 110, 112), 0.4); touched = true; np += 1
            elseif (n == 'tile_red_a' or n == 'tile_red_b') and (seed % 5 ~= 0) then
              p.Color = (n == 'tile_red_a') and r or r:Lerp(Color3.new(0, 0, 0), 0.14); touched = true; np += 1
            end
          end
        end
        if touched then m:SetAttribute('RoofVaried2', true); nm += 1 end
      end
    end
  end
end
return string.format('capital roofs recoloured: %d parts on %d buildings', np, nm)

