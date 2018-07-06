from wv_util import chip_image, get_labels
from os import path, listdir
from PIL import Image
import numpy as np

def makeDir(imFolder, outFolder, labelFile, dirFile, classRef, res=(300,300)):
    coords, imNames, classes = get_labels(labelFile)
    print('Got labels')
    imFiles = listdir(imFolder)
    with open(dirFile, 'w') as outFile:
        for im in imFiles:
            if im.endswith('.tif'):
                arr = np.array(Image.open(path.join(imFolder, im)))
                chips, boxes, boxClasses = chip_image(arr, coords[imNames == im], classes[imNames == im], res)
                
                for i in range(len(chips)):
                    chip = Image.fromarray(chips[i])
                    newName = path.join(outFolder, "{}_{}.jpg".format(im[:-4], i))
                    chip.save(newName)
                    boxStr = []
                    emptyChip = False
                    for j in range(len(boxes[i])):
                        box = boxes[i][j]
                        boxClass = boxClasses[i][j]
                        if boxClass == 0:
                            emptyChip = True
                        classID = getRealID(int(boxClasses[i][j]), classRef)
                        boxStr.append("{},{},{},{},{}".format(int(box[0]), int(box[1]), int(box[2]), int(box[3]), classID))
                    if not emptyChip:
                        infoStr = '{} {}\n'.format(newName, " ".join(boxStr))   
                        outFile.write(infoStr)
                    # print(newName)

            print(im)       

def getRealID(oldID, classes):
    try: 
        return classes.index(str(oldID))
    except Exception:
        return 60  
                      

if __name__ == "__main__":
    imFolder = '/srv/etc-str-01/project/xview/datasets/xview/trainImages'
    outFolder = 'trainChips'
    labelFile = '/srv/scratch/xview/data_utilities/xView_train.geojson'
    dirFile = 'trainDir.txt'
    with open('/srv/scratch/xview/data_utilities/xview_class_labels.txt', 'r') as f:
        classStr = f.read()
    classes = classStr.split('\n')
    classes = [ x[0:2] for x in classes ]
    print(classes)

    makeDir(imFolder, outFolder, labelFile, dirFile, classes)
