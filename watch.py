import pandas as pd
import matplotlib.pyplot as plt
import os
import time
from pathlib import Path

project_path = Path(os.path.abspath('__file__')).parent
log_path = project_path / 'population' / 'log.csv'
print(f'log_path {log_path}')

df = pd.read_csv(log_path)

while True:
    fig, (ax1, ax2, ax3) = plt.subplots(1,3,figsize=(30, 12))
    ax1.title.set_text = 'Steps'
    ax1.errorbar(df.index, df.steps_mean, df.steps_std, fmt='ok', ecolor='green', lw=3)
    ax1.errorbar(df.index, df.steps_mean, [df.steps_mean-df.steps_min, df.steps_max-df.steps_mean], fmt='.k', ecolor='gray', lw=1)

    ax2.title.set_text = 'Apple'
    ax2.errorbar(df.index, df.apples_mean, df.apples_std, fmt='ok', ecolor='green', lw=3)
    ax2.errorbar(df.index, df.apples_mean, [df.apples_mean-df.apples_min, df.apples_max-df.apples_mean], fmt='.k', ecolor='gray', lw=1)

    ax3.title.set_text = 'Fitness'
    ax3.errorbar(df.index, df.fitness_mean, df.fitness_std, fmt='ok', ecolor='green', lw=3)
    ax3.errorbar(df.index, df.fitness_mean, [df.fitness_mean-df.fitness_min, df.fitness_max-df.fitness_mean], fmt='.k', ecolor='gray', lw=1)
    
    plt.show()
    time.sleep(1)
    plt.clf()