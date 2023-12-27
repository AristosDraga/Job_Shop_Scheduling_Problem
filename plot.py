from jacksonpy import JacksonAlgo
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

# Processing order of jobs from the SPT dispatching rule solving.
data = [3, 2, 9, 5, 1, 2, 8, 9, 2, 3, 1, 5, 5, 8, 3, 8, 3, 6, 10, 9, 9, 2, 1, 6, 1, 4, 8, 6, 5, 4, 7, 2, 10, 4, 4, 7, 10, 4, 6, 10, 5, 8, 7, 7, 6, 7, 1, 10, 3, 9]

# Split the processing times list into sublists for each job
jobs = [data[i:i+5] for i in range(0, len(data), 5)]

# Insert job indices at the beginning of each sublist
data = [[i+1] + job for i, job in enumerate(jobs)]


al = JacksonAlgo.JackAlgo(data)

print(al)

preparedData = al.prepareData()

cmaxVirtual, _, __ = al.get_cmax_virtual(preparedData)


result = al.solve(cmaxVirtual)

al.generate_pdf_file(results=result)

img = np.asarray(Image.open('./output/ImagesOutput/Gantt_Chart_virtual0_cmax_(91).png'))
imgplot = plt.imshow(img)
plt.show()
