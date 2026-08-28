import csv
import matplotlib.pyplot as plt
import os

data = []
filenames = []
for file in os.listdir("RewardLogs"):
    if file.endswith(".csv"):        
        with open('RewardLogs/' + file, 'r') as f:                
            reader = csv.reader(f)
            data.append(list(reader))
            filenames.append(file[7:-4])
rewards = []
episodecount = []
framecount = []
length = []
print(filenames)
for list in data:
    rewards.append([float(row[0]) for row in list])
    episodecount.append([int(row[1]) for row in list])
    framecount.append([int(row[2]) for row in list])
    length.append([int(row[3]) for row in list])

for i in range(len(rewards)):
    print(f"max snake length for run {i+1}: {max(length[i])}, max reward: {max(rewards[i])}, total frames: {framecount[i][-1]}")
    plt.scatter(episodecount[i], rewards[i], label=f"Run {i+1}")
    plt.xlabel('Episode')
    plt.ylabel('Reward')
    plt.title('Training Rewards')
    plt.legend()
    plt.savefig(f"Plots/TrainingRewards_{filenames[i]}.png")
    plt.close()

    running_average_length = []
    window_size = 10
    for j in range(len(length[i])):
        if j < window_size:
            running_average_length.append(sum(length[i][:j+1])/(j+1))
        else:
            running_average_length.append(sum(length[i][j-window_size:j+1])/(window_size))
    plt.plot(episodecount[i], running_average_length,color='red', label=f"Run {i+1}")
    plt.scatter(episodecount[i], length[i], label=f"Run {i+1}")
    plt.xlabel('Episode')
    plt.ylabel('Snake Length')
    plt.title('Snake Length over Episodes')
    plt.legend()
    plt.savefig(f"Plots/SnakeLength_{filenames[i]}.png")
    plt.close()

    framedelta = [framecount[i][j] - framecount[i][j-1] for j in range(1, len(framecount[i]))]

    plt.scatter(episodecount[i][1:], framedelta)
    plt.xlabel('Episode')
    plt.ylabel('Frame Delta')
    plt.title('Frame Delta over Episodes')
    plt.savefig(f"Plots/FrameDelta_{filenames[i]}.png")
    plt.close()

    plt.scatter(length[i], rewards[i])
    plt.xlabel('Snake Length')
    plt.ylabel('Reward')
    plt.title('Reward over Snake Length')
    plt.legend()
    plt.savefig(f"Plots/RewardOverSnakeLength_{filenames[i]}.png")
    plt.close()