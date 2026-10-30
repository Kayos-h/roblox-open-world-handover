-- glow_fix2: parts still named glow* inside the elf valley become plain warm cream; also checks the colour of what remains
local function inElf(p) return p.X > -2200 and p.X < -1000 and p.Z > -1100 and p.Z < 200 end
local n, ex = 0, {}
for _, d in ipairs(workspace:GetDescendants()) do
  if d:IsA('BasePart') and inElf(d.Position) then
    local nm = string.lower(d.Name)
    if string.find(nm, 'glow', 1, true) or string.find(nm, 'neon', 1, true) then
      if #ex < 6 then ex[#ex + 1] = string.format('%s mat=%s rgb(%d,%d,%d)', d.Name, d.Material.Name, d.Color.R * 255, d.Color.G * 255, d.Color.B * 255) end
      d.Material = Enum.Material.SmoothPlastic
      d.Color = Color3.fromRGB(222, 206, 172)
      d.Name = 'lamp_pane'
      n += 1
    end
  end
end
return string.format('glow-named parts made plain: %d\n%s', n, table.concat(ex, '\n'))
