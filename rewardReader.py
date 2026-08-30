import csv
import matplotlib.pyplot as plt
import os
import numpy as np
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

filenames.append("combined")
print(filenames)
for list in data:
    rewards.append([float(row[0]) for row in list])
    episodecount.append([int(row[1]) for row in list])
    framecount.append([int(row[2]) for row in list])
    length.append([int(row[3]) for row in list])
framecount[-7] = [framecount[-7][i] + framecount[20][-1] for i in range(len(framecount[-7]))]
framecount.append(framecount[20]+framecount[-7])
rewards.append(rewards[20]+rewards[-7])
length.append(length[20]+length[-7])
episodecount.append(episodecount[20]+episodecount[-7])
for i in range(len(rewards)):
    print(f"max snake length for run {i+1}: {max(length[i])}, max reward: {max(rewards[i])}, total frames: {framecount[i][-1]}")

    running_average_reward = []
    window_size = 100
    for j in range(len(rewards[i])):
        if j < window_size:
            running_average_reward.append(sum(rewards[i][:j+1])/(j+1))
        else:
            running_average_reward.append(sum(rewards[i][j-window_size:j+1])/(window_size))

    plt.plot(framecount[i], running_average_reward,color='red', label=f"average reward over {window_size} episodes")
    plt.scatter(framecount[i], rewards[i], label=f"reward", alpha=0.8)
    plt.xlabel('Frames')
    plt.ylabel('Reward')
    # plt.title('Training Rewards')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"Plots/TrainingRewards_{filenames[i]}.pdf")
    plt.close()

    running_average_length = []
    window_size = 100
    for j in range(len(length[i])):
        if j < window_size:
            running_average_length.append(sum(length[i][:j+1])/(j+1))
        else:
            running_average_length.append(sum(length[i][j-window_size:j+1])/(window_size))
    plt.plot(framecount[i], running_average_length,color='red', label=f"average snake length over {window_size} episodes")
    plt.scatter(framecount[i], length[i], label=f"snake length", alpha=0.5)
    plt.xlabel('Frames')
    plt.ylabel('Snake Length')
    # plt.title('Snake Length over Episodes')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"Plots/SnakeLength_{filenames[i]}.pdf")
    plt.close()

    framedelta = [framecount[i][j] - framecount[i][j-1] for j in range(1, len(framecount[i]))]

    plt.scatter(framecount[i][1:], framedelta)
    plt.xlabel('Frames')
    plt.ylabel('Frame Delta')
    # plt.title('Frame Delta over Episodes')
    plt.savefig(f"Plots/FrameDelta_{filenames[i]}.png")
    plt.close()

    plt.scatter(length[i], rewards[i])
    plt.xlabel('Snake Length')
    plt.ylabel('Reward')
    # plt.title('Reward over Snake Length')
    plt.legend()
    plt.savefig(f"Plots/RewardOverSnakeLength_{filenames[i]}.png")
    plt.close()