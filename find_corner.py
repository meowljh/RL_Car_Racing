import cv2
from scipy.signal import find_peaks
import matplotlib.pyplot as plt


img = cv2.imread('track_2.png')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
fig, ax = plt.subplots(1, 1)
ax.imshow(img)
corners = [
    (800, 110),
    (175, 600),
    (560, 400),
    (925, 645),
    (1085, 490),
    (1440, 365)
]

# for (x, y) in corners:
for ci, (x, y) in enumerate(corners):
    ax.scatter([x], [y], s=10)
    ax.text(x, y, s=str(ci), c ='w')
plt.show()

fig.savefig("track_2_corner.png")