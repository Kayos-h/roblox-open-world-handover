p = r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\v4\scan_colors2.luau'
t = open(p, encoding='utf-8').read()
t = t.replace("string.format('%-100s x%d', k, v)", "string.format('%s  x%d', k, v)")
t = t.replace("string.format('%-48s parts=%d vol=%.0f', k, v.n, v.vol)", "string.format('%s  parts=%d vol=%.0f', k, v.n, v.vol)")
open(p, 'w', encoding='utf-8').write(t)
print('format widths removed')
