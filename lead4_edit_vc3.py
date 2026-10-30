"""lead4_edit_vc3 - kit order (prune before post) and warmer low band for the portals."""
S = r"C:\Users\Nitro\.kiro\crew\workspace\town"


def edit(path, pairs):
    t = open(path, encoding='utf-8-sig').read()
    for old, new in pairs:
        assert t.count(old) == 1, (path, t.count(old), old[:80])
        t = t.replace(old, new)
    open(path, 'w', encoding='utf-8').write(t)


edit(S + r"\library\src\v5_leadkit.py", [("""    if cfg.get('post'):
        cfg['post'](self)
    for rule in cfg.get('prune') or []:
        _prune(self, rule)
""", """    for rule in cfg.get('prune') or []:
        _prune(self, rule)
    if cfg.get('post'):
        cfg['post'](self)
"""), ("Order inside the hook: deform -> post -> prune -> normals", "Order inside the hook: deform -> prune -> post -> normals")])
edit(S + r"\lead4_snip_vc.py", [("RAMP_A = [P['rock_d'], PBR['rock_b'], PBR['rock_c'], P['rock_w'], P['rock_l']]", "RAMP_A = [PBR['rock_b'], PBR['rock_c'], P['rock_w'], P['rock_l']]"),
                                ("RAMP_B = [P['rock_m'], PBR['rock_c'], P['rock_w'], P['rock_l']]", "RAMP_B = [PBR['rock_b'], PBR['rock_c'], P['rock_w'], P['rock_l'], P['rock_w']]")])
print('ok')
