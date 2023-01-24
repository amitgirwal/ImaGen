import cv2
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('seaborn')

loaded_img = cv2.imread("image1.jpg")
Sepia_Kernel = np.array([[0.272, 0.534, 0.131],[0.349, 0.686, 0.168],[0.393, 0.769, 0.189]])
Sepia_Effect_Img = cv2.filter2D(src=loaded_img, kernel=Sepia_Kernel, ddepth=-1)
plt.figure(figsize=(8,8))
plt.imshow(Sepia_Effect_Img,cmap="gray")
plt.axis("off")
plt.show()