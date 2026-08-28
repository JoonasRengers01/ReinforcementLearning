import csv
import matplotlib.pyplot as plt
import os

data = []

for file in os.listdir("RewardLogs"):
    if file.endswith(".csv"):        
        with open('RewardLogs/' + file, 'r') as f:                
            reader = csv.reader(f)
            data.append(list(reader))

rewards = [float(row[0]) for row in data]
episodecount = [int(row[1]) for row in data]
framecount = [int(row[2]) for row in data]
length = [int(row[3]) for row in data]


plt.scatter(episodecount, rewards)
plt.xlabel('Episode')
plt.ylabel('Reward')
plt.title('Training Rewards')
plt.show()

plt.scatter(episodecount, length)
plt.xlabel('Episode')
plt.ylabel('Snake Length')
plt.title('Snake Length over Episodes')
plt.show()

framedelta = [framecount[i] - framecount[i-1] for i in range(1, len(framecount))]

plt.scatter(episodecount[1:], framedelta)
plt.xlabel('Episode')
plt.ylabel('Frame Delta')
plt.title('Frame Delta over Episodes')
plt.show()

plt.scatter(length, rewards)
plt.xlabel('Snake Length')
plt.ylabel('Reward')
plt.title('Reward over Snake Length')
plt.show()