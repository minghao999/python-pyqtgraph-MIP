import numpy as np
import os

def imgnp(file,sizes):
    try:
        if sizes==512:
            imgfile=np.fromfile(file,dtype='uint16')
            img=imgfile[256:262144+256]
            img.shape=(sizes,sizes)
            return True,img
        elif sizes==256:
            imgfile=np.fromfile(file,dtype='uint16')
            img=imgfile[256:65536+256]
            img.shape=(sizes,sizes)
            return True,img
        else:
            return False,None
    except FileNotFoundError:
        return False,None

def imgnpAuot(file):
    try:
        try:
            imgfile=np.fromfile(file,dtype='uint16')
            img=imgfile[256:262144+256]
            img.shape=(512,512)
            return True,img
        except:
            imgfile=np.fromfile(file,dtype='uint16')
            img=imgfile[256:65536+256]
            img.shape=(256,256)
            return True,img
        
    except FileNotFoundError:
        return False,None
    except ValueError:
            return False,None


def read_images(path):
    images = []
    for (root, directories, files) in os.walk(path):
        files.sort()
        if len(files) >100:
            for file in files:
                try:
                    try:
                        imgfile=np.fromfile(os.path.join(root, file),dtype='uint16')
                        img=imgfile[256:262144+256]
                        img.shape=(512,512)
                        images.append(img)
                    except:
                        imgfile=np.fromfile(os.path.join(root, file),dtype='uint16')
                        img=imgfile[256:65536+256]
                        img.shape=(256,256)
                        images.append(img)
                except FileNotFoundError:
                    return False,None
                except ValueError:
                    return False,None
            return True,images
        else:
            return False,None
    