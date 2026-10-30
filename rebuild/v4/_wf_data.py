import json
p = json.load(open(r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\v4\waterfall_path.json'))
json.dump({'path': p}, open(r'C:\Users\Nitro\.kiro\crew\workspace\town\rebuild\v4\waterfall_data.json', 'w'))
print('waterfall data:', len(p), 'points')
