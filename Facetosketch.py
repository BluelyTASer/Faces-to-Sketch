from datetime import datetime
import os
filenameextensions = [".tif", ".tiff", ".bmp", ".dib", ".jpg", ".jpeg", ".jpe", "jif", "jfif", ".jfi", ".gif", ".png", ".eps", ".raw", ".arw", ".cr2", ".nrw", ".k25", ".nef", ".orf", ".sr2", ".svg", ".svgz", ".ai", ".eps", ".webp", ".heif", ".heic", ".jp2", ".j2k", ".jpf", ".jpx", ".jpm", ".mj2"]
try:  
  import tkinter as tk
except:
   raise ImportError("You should install tkinter!")
try:  
  import numpy as np
except:
  os.system("pip install numpy")
  try:
    import numpy as np
  except:
    raise ImportError("Unable to Import! Check Python Version!")
try:  
  import imageio
except:
  os.system("pip install imageio")
  try:
    import imageio
  except:
    raise ImportError("Unable to Import! Check Python Version!")
try:  
  import scipy.ndimage
except:
  os.system("pip install scipy")
  try:
    import scipy.ndimage
  except:
    raise ImportError("Unable to Import! Check Python Version!")
try:  
  import cv2
except:
  os.system("pip install opencv-python")
  try:
    import cv2
  except:
    raise ImportError("Unable to Import! Check Python Version!")
try:  
  from face_extractor import Extractor
except:
   os.system("pip install FaceExtractor")
   try:  
     from face_extractor import Extractor
   except:
     raise ImportError("Unable to Import! Check Python Version!")
from tkinter import filedialog
from shutil import copyfile,rmtree
root = tk.Tk()
root.withdraw()
root.iconbitmap(r"icon.ico")
pathname = filedialog.askopenfilename(title="Open a image", filetypes=[("image files", (".tif", ".tiff", ".bmp", ".dib", ".jpg", ".jpeg", ".jpe", "jif", "jfif", ".jfi", ".gif", ".png", ".eps", ".raw", ".arw", ".cr2", ".nrw", ".k25", ".nef", ".orf", ".sr2", ".svg", ".svgz", ".ai", ".eps", ".webp", ".heif", ".heic", ".jp2", ".j2k", ".jpf", ".jpx", ".jpm", ".mj2"))])
currentlydirectory = filedialog.askdirectory(title="Select which directory to save converted faces to sketch on")
root.destroy()
basename = str(os.path.basename(pathname))
basename1 = str(os.path.basename(pathname))
if not os.path.exists(pathname):
  raise FileNotFoundError("Image has not been found")
if not os.path.exists(currentlydirectory):
  raise Exception("Directory has not been found")
if (not basename[basename.rfind("."):] in filenameextensions) or (not basename[basename.rfind("."):].lower() in filenameextensions):
  basename = str(basename) + ".png"
if os.path.exists(basename):
  count = 1
  basename2 = basename
  while os.path.exists(basename):
    basename = basename2
    for x in filenameextensions:
      basename = basename.replace(str(x), "-" + str(count) + str(x))
    count += 1
    if count > 10000:
      print("Risk to overwrite, proceed to converting face to sketch instead to avoid system overload")
      break
originaldirectory = os.getcwd()
if not os.path.exists(os.path.join(currentlydirectory, "faces")):
  os.chdir(currentlydirectory)
  os.mkdir("faces")
  os.chdir(originaldirectory)
else:
  if os.path.isfile(os.path.join(currentlydirectory, "faces")):
    os.chdir(currentlydirectory)
    os.mkdir("faces")
    os.chdir(originaldirectory)
aaa = datetime.now()
facersr = str(os.path.join(currentlydirectory, "faces"))
copyfile(pathname, os.path.join(facersr, basename1))
face_locations = Extractor.extract(os.path.join(facersr, basename1))
def grayscale(rgb):
	return np.dot(rgb[...,:3],[0.299,0.587,0.114])
def dodge(front,back):
	result=front*255/(255-back)
	result[result>255]=255
	result[back==255]=255
	return result.astype('uint8')
if len(face_locations) > 1:
  print(str(len(face_locations)) + " found faces!")
  getlocation = str(os.path.join(currentlydirectory, "faces"))
  for filenamersr in os.listdir(getlocation):
    if os.path.isfile(os.path.join(getlocation, filenamersr)):
      if not basename1 == filenamersr and basename[:basename.rfind(".")] in filenamersr:
        s=imageio.imread(os.path.join(getlocation, filenamersr))
        g=grayscale(s)
        i=255-g
        b=scipy.ndimage.filters.gaussian_filter(i,sigma=10)
        r=dodge(b,g)
        filename = filenamersr
        cv2.imwrite(os.path.join(currentlydirectory, filename),r)
  rmtree(facersr)
elif len(face_locations) == 1:
  print("1 found face!")
  getlocation = str(os.path.join(currentlydirectory, "faces"))
  for filenamersr in os.listdir(getlocation):
    if os.path.isfile(os.path.join(getlocation, filenamersr)):
      if not basename1 == filenamersr:
        s=imageio.imread(os.path.join(getlocation, filenamersr))
        g=grayscale(s)
        i=255-g
        b=scipy.ndimage.filters.gaussian_filter(i,sigma=10)
        r=dodge(b,g)
        filename = filenamersr
        cv2.imwrite(os.path.join(currentlydirectory, filename),r)
  rmtree(facersr)
else:
  print("No faces found.")
  rmtree(facersr)
print(datetime.now() - aaa)
