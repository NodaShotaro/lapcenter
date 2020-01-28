
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

runner = pd.read_csv('runner.csv',encoding='cp932')
leg = pd.read_csv('leg.csv',encoding='cp932')

df = pd.merge(runner,leg)
df.to_csv('join.csv',encoding='cp932')

plt.scatter(abe['difficulty'],abe['legSpeed'])
plt.xlabel('Difficulty')
plt.ylabel('LegSpeed')
plt.ylim(50,500)

plt.savefig('abe.png')