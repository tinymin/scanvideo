from PIL import Image
from moviepy.editor import VideoFileClip
import sys
import os
import shutil
import pytesseract

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def help():
  print("** scanvideo.py")
  print("")
  print("Usage : python3 vailadTxtFromImg.py [Options] <Video File>")
  print("Usage : python3 vailadTxtFromImg.py [Options] <Video File1> <Video File2> <Video File3>...")
  print("")
  print("Option")
  print("  --i <Path>          : 설정한 경로에 오염된 파일을 격리시킵니다.")
  print("  --r                 : 오염된 파일을 삭제합니다. --i 옵션과 함께 쓰는 경우 무시됩니다.")
  print("  --f 1,6,10,12...    : 설정한 프레임을 체크합니다.")
  print("  --t                 : 모든 프레임을 체크합니다. --f 옵션과 함께 쓰는 경우 무시됩니다.")
  print("")
  print("")

def supportExt(ext):
  supportExtList = [".mkv", ".avi", ".mp4", ".mpg"]

  if(ext.lower() in supportExtList):
    return True
  return False

def scanFile(filePath, options):
  ext = os.path.splitext(filePath)[1]

  if (False == supportExt(ext)):
    return False

  try:
    video = VideoFileClip(filePath)
  except IndexError:
    print(str(" [" + bcolors.WARNING + "{:>11}" + bcolors.ENDC + "] " + filePath).format("Not support"))
    return False
  except OSError:
    print(str(" [" + bcolors.WARNING + "{:>11}" + bcolors.ENDC + "] " + filePath).format("Not support"))
    return False
  except UnicodeDecodeError:
    print(str(" [" + bcolors.WARNING + "{:>11}" + bcolors.ENDC + "] " + filePath).format("Not support"))
    return False
  except KeyError:
    print(str(" [" + bcolors.WARNING + "{:>11}" + bcolors.ENDC + "] " + filePath).format("Not support"))
    return False

  isInfected = False
  fileName = os.path.basename(filePath)
  destPath = options["destPath"]
  chkFrames = options["chkFrames"] if(len(options["chkFrames"]) !=0) else [4, 3, 2, 1, 0] # 디폴트 체크 프레임 [4, 3, 2, 1, 0]
  isTestMode = options["isTestMode"]
  duration = int(video.duration)
  if(True == isTestMode):
    chkFrames = range(0, duration)

  # 비디오를 검사한다.
  for i in chkFrames:
    # 비디오의 길이를 넘어가면 예외처리
    if(i > duration):
      continue

    f = video.get_frame(i)
    image = Image.fromarray(f, 'RGB')
    txt = pytesseract.image_to_string(image)
    if(True == isTestMode):
      print("------ frame = (" + str(i) + "/" + str(duration) + "),  " +  filePath + " ------")
      print(txt)

    if "sex" in txt or "500" in txt:
      print(" [" + bcolors.FAIL + "{:>11}".format("Infected") + bcolors.ENDC + "] " + filePath, end='')
      procMsg = ""
      if (True == isDeleteFile):
        procMsg = bcolors.FAIL + "  - Deleting..." + bcolors.ENDC
        print(procMsg, end='')
        os.remove(filePath)
        print(" - Done", end='')

      if ("" != destPath):
        if ("/" != destPath[-1:]):
          destPath = destPath + "/"
        destPath = destPath + fileName
        procMsg = bcolors.OKGREEN + "  - Moving..." + bcolors.ENDC
        print(procMsg, end='')
        shutil.move(filePath, destPath)
        print(" - Done", end='')

      print("")
      isInfected = True
      break

  if (False == isInfected):
    print(" [" + bcolors.OKGREEN + "{:>11}".format("Normal") + bcolors.ENDC + "] " + filePath)


# Start Main
argc = len(sys.argv)
if (1 == argc) :
  help()
  sys.exit()

isDeleteFile = False
isTestMode = False
filePos = 0
destPath = ""
chkFrames = []
wrongArgs = ["-i", "-r", "-t", "-f"]
# 매개변수 처리
for i in range(1,len(sys.argv)):
  arg = sys.argv[i]
  if (arg in wrongArgs ):
    help()
    sys.exit()

  if (0 == filePos and "--r" == arg):
    isDeleteFile = True
    filePos = i

  if("--i" == arg):
    destPath = sys.argv[i+1]
    filePos = i + 1
    isDeleteFile = False

  if(0 == len(chkFrames) and "--t" == arg):
    print("Test mond on!")
    isTestMode = True

  if("--f" == arg):
    chkFrames = list(map(int, sys.argv[i+1].split(',')))
    isTestMode = False

# 매개변수 예외 처리
filePos = filePos + 1
if (filePos == argc):
  help()
  sys.exit()

if("" != destPath and os.path.isdir(destPath) == False):
  print("Path is not exist or is not directory! < " + destPath + " >")
  sys.exit()

# 옵션 세팅
options = {"destPath":destPath, "chkFrames":chkFrames, "isTestMode":isTestMode}

# 파일 검사 시작
for i in range(filePos,len(sys.argv)):
  scanFile(sys.argv[i], options)
