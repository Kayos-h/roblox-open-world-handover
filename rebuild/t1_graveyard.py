import json, math
from layout_lib import Plan
import towns3 as T

P = Plan('town1_graveyard', seed=909)
gcx, gcz, grot = -238.0, 246.0, 90.0
T.graveyard(P, gcx, gcz, grot, 42, 52, 'Graveyard', fence='A103_fence_iron', rows=9, mausoleums=2, density=0.88)
t = math.radians(grot)
ux, uz = (math.cos(t), -math.sin(t)), (math.sin(t), math.cos(t))
def gpt(a, b):
    return (gcx + ux[0] * a + uz[0] * b, gcz + ux[1] * a + uz[1] * b)
# flowers and candles on some graves, benches, lanterns along the aisle, cypress-like pines
for it in [i for i in P.items if i['model'].startswith('D1') and i['model'] != 'D17_mausoleum' and i['model'] != 'D18_graveyard_gate' and i['model'] != 'D19_weeping_statue'][::3]:
    P.put(P.rng.choice(['A43_flowers_red', 'A46_flowers_white', 'A45_flowers_purple']), it['x'] + P.rng.uniform(-1.5, 1.5), it['z'] + P.rng.uniform(-1.5, 1.5), P.rng.uniform(0, 360), 'Graveyard', block=False, check=False, scale=0.7)
for b in range(-40, 41, 16):
    P.put('A19_hanging_lantern' if b % 32 else 'A17_lamp_wood_rustic', *gpt(4.5, b), grot, 'Graveyard', block=False, check=False)
for b in (-20, 12):
    P.put('A83_bench_stone', *gpt(-5, b), grot + 90, 'Graveyard', block=False, check=False)
for (a, b) in ((-38, -48), (38, -48), (-38, 10), (38, 30), (-38, 46), (38, -10)):
    P.put('A31_pine_3', *gpt(a, b), P.rng.uniform(0, 360), 'Graveyard', block=False, check=False, scale=P.rng.uniform(0.9, 1.2))
for k in range(8):
    P.put('A23_candle_cluster', *gpt(P.rng.uniform(-30, 30), P.rng.uniform(-40, 40)), 0, 'Graveyard', block=False, check=False, scale=0.6)
P.save(r'C:\Users\Nitro\.kiro\crew\workspace\town\mapplan\town1_graveyard.json')
print(len(P.items))
