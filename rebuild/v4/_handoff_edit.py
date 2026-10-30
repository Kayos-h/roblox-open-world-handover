p = r'C:\Users\Nitro\.kiro\crew\workspace\town\HANDOFF_v4_map.md'
t = open(p, encoding='utf-8-sig').read()
marker = '- Terrain: `WriteVoxels(Water)`'
note = ('- Terrain grass blades: `Terrain.Decoration` and `Terrain.GrassLength` are NOT reachable from scripts (they are not valid members for plugin code). '
        'They live only in the Properties panel: select Terrain (`Selection:Set({workspace.Terrain})`), click the GrassLength value cell (screen about (1737,244)), '
        'type with `town\\type_focus.ps1 -text 0.3` (SendKeys into the focused cell). It is set to 0.3 now (default 0.7). Reviewers kept seeing chest-high blades '
        'until this was changed; the grass MODELS were never the main cause. Verify by capturing the right-hand panel strip only (never the 3D view).\n')
assert marker in t, 'marker missing'
t = t.replace(marker, note + marker, 1)
open(p, 'w', encoding='utf-8').write(t)
print('grass note added')
