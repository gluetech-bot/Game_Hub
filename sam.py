import matplotlib.pyplot as plt

labels = ['A', 'B', 'C']
sizes = [30, 45, 25]

explode = [0, 0.1, 0]   # only B is separated

plt.pie(sizes, labels=labels, explode=explode, autopct='%1.1f%%')
plt.axis('equal')
plt.show()