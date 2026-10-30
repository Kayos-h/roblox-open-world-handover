-- b13: invisible NPC spawn markers for later gameplay (no NPCs yet)
local L = _G.L
local V, CF = L.V, L.CF
local town = workspace:FindFirstChild('SpawnTown')
local f = L.folder(town, 'NPCMarkers')

local n = 0
local function mark(role, x, z, fx, fz, yOverride)
	local y = yOverride or L.ground(x, z)
	local p = Instance.new('Part')
	p.Name = 'NPC_' .. role
	p.Size = V(2, 5, 1)
	local pos = V(x, y + 2.5, z)
	p.CFrame = CF(pos, pos + V(fx, 0, fz))
	p.Anchored, p.CanCollide, p.CanTouch, p.CanQuery = true, false, false, false
	p.Transparency = 1
	p:SetAttribute('NPCRole', role)
	p:SetAttribute('Reserved', true)
	p:SetAttribute('Facing', V(fx, 0, fz).Unit)
	p.Parent = f
	n += 1
end

-- plaza / civic
mark('Greeter', 0, 70, 0, -1)
mark('TownCrier', -24, 20, 1, 0)
-- skull HQ (v4: entrance faces the forecourt at z≈-470)
mark('HQGuard', -16, -490, 0, 1, nil)
mark('HQGuard', 16, -490, 0, 1, nil)
mark('Captain', 0, -470, 0, 1, nil)
-- landmarks
mark('TavernKeeper', 110, -38, 1, 0)
mark('GuildReceptionist', 112, 48, 0, -1)
mark('QuestBoardClerk', 100, 18, 0, -1)
-- crafts
mark('Blacksmith', 366, 64, -1, 0)
mark('Priest', -190, -300, 1, 0)
mark('CombatTrainer', 200, -290, 1, 0)
-- farm
mark('Farmer', 180, 322, 0, 1)
mark('Miller', 360, 345, -1, 0)
-- mage tower
mark('Archmage', -240, 360, 1, 0)
mark('RuneScholar', -260, 395, 0, -1)
-- gates (wall line at +/-425)
for _, s in ipairs({-1, 1}) do
	mark('GateGuard', s*8, 405, 0, 1)
	mark('GateGuard', 405, s*8, 1, 0)
	mark('GateGuard', -405, s*8, -1, 0)
end

-- shopkeepers behind each market stall
local market = town:FindFirstChild('Market')
local shops = 0
if market then
	for _, m in ipairs(market:GetDescendants()) do
		if m:IsA('Model') and m.Name:lower():find('stall') and shops < 14 then
			local cf = m:GetPivot()
			local back = cf.Position - cf.LookVector*3
			mark('Shopkeeper', back.X, back.Z, cf.LookVector.X, cf.LookVector.Z)
			shops += 1
		end
	end
end

return string.format('npc markers ok n=%d shops=%d', n, shops)
