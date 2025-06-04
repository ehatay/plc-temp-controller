import matplotlib.pyplot as plt
import csv
from collections import defaultdict

def readCSV(filepath):
    data = defaultdict(list)
    with open(filepath, newline="") as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            for key, value in row.items():
                data[key.strip()].append(value.strip())
    return data

def plotCombined(files, max_samples=2300):
    num_files = len(files)
    fig, axes = plt.subplots(num_files, 1, figsize=(14, 5 * num_files), sharex=False)

    if num_files == 1:
        axes = [axes]

    for i, (filepath, ax) in enumerate(zip(files, axes), start=1):
        data = readCSV(filepath)

        SW0_State = [value.lower() in ['1', 'true', 'yes'] for value in data['SW0_State'][:max_samples]]
        Temp = list(map(float, data['Temp'][:max_samples]))
        SP = list(map(float, data['PID.SP'][:max_samples]))
        ERR = list(map(float, data['PID.ERR'][:max_samples]))
        OUT = list(map(float, data['PID.OUT'][:max_samples]))
        KP = float(data['PID.KP'][0])
        KI = float(data['PID.KI'][0])
        KD = float(data['PID.KD'][0])
        x = list(range(len(Temp)))

        absolute_errors = [abs(t - s) for t, s in zip(Temp, SP)]

        mean_absolute_error = sum(absolute_errors) / len(Temp) if Temp else 0


        for j, state in enumerate(SW0_State):
            if state:
                ax.axvspan(j - 0.5, j + 0.5, color='blue', alpha=0.1)

        ax.plot(x, Temp, label='Temp', color='red', linewidth=2)
        ax.plot(x, SP, label='PID.SP', color='green', linestyle='--')
        ax.plot(x, ERR, label='PID.ERR (Original)', color='orange', linestyle=':')
        ax.plot(x, OUT, label='PID.OUT', color='purple', linestyle='-.')

        ax.plot([], [], ' ', label=f'PID.KP = {KP:.2f}')
        ax.plot([], [], ' ', label=f'PID.KI = {KI:.2f}')
        ax.plot([], [], ' ', label=f'PID.KD = {KD:.2f}')

        ax.set_title(f'Dataset {i}: {filepath} | Mean Absolute Error = {mean_absolute_error:.3f}')
        ax.set_ylabel('Value')
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.legend()

    axes[-1].set_xlabel('Sample Index')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    filepaths = [
        'data/output_1.csv',
        'data/output_2.csv',
        'data/output_3.csv'
    ]
    plotCombined(filepaths)