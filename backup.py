from genericpath import isfile
from posixpath import basename
from pyhocon import ConfigFactory
import time, os, shutil, socket
from pathlib import Path

hostname = socket.gethostname()


def mkdirIfNotExist(dirPath):
    if not Path.is_dir(dirPath):
        Path.mkdir(dirPath, parents=True)


#备份配置
config = ConfigFactory.parse_file('config/base.conf')
#备份目录
backupPath = Path(config.backupPath)
mkdirIfNotExist(backupPath)
#临时目录，先清空
tmpPath = Path(backupPath, "tmp")
if Path.exists(tmpPath):
    shutil.rmtree(tmpPath)
mkdirIfNotExist(tmpPath)

#时间戳
ticks = int(time.time())
date = time.strftime("%Y_%m_%d", time.localtime())

#备份文件名
backupFileName = f"{hostname}_{date}_{ticks}"
backupFilePath = Path(backupPath, backupFileName)
for conf in config.backupList:
    srcPath = Path(conf.srcPath)
    name = srcPath.name
    destPath = "" if "destPath" not in conf else Path(conf.destPath)
    destPath = Path(tmpPath, destPath)
    destName = name if "destName" not in conf else conf.destName
    destName = Path(destPath, destName)
    if Path.exists(srcPath):
        mkdirIfNotExist(destName.parent)
        if Path.is_dir(srcPath):
            shutil.copytree(srcPath, destName)
        elif Path.is_file(srcPath):
            shutil.copy(srcPath, destName)

shutil.make_archive(backupFilePath, "gztar", tmpPath)
shutil.rmtree(tmpPath)