local G = _G.FILL2
if not G then return "no FILL2" end
local out = { string.format("tag=%s %d/%d done=%s deletedVox=%d (cols %d, max %d studs) filledVox=%d (cols %d) errs=%d secs=%s", tostring(G.tag), G.i, G.n, tostring(G.done), G.deletedVox, G.delCols, G.maxdel, G.filledVox, G.fillCols, #G.errs, tostring(G.secs)) }
for i = 1, math.min(8, #G.errs) do table.insert(out, G.errs[i]) end
return table.concat(out, "\n")
