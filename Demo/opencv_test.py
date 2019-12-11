import cv2
import numpy as np

fileName = r'C:\Users\Cjay\Desktop\Test\Bathymetry-of-Great-Slave-Lake-Schertzer-et-al-2000_W640.jpg'
fileName2 = r'C:\Users\Cjay\Desktop\Test中文\Fig.png'
openfile_name_gbk = fileName2.encode('gbk')

img = cv2.imdecode(np.fromfile(fileName2, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
#img = cv2.imread(openfile_name_gbk.decode())
cv2.namedWindow("test")
cv2.imshow("test", img)
cv2.waitKey(0)
cv2.destroyAllWindows()