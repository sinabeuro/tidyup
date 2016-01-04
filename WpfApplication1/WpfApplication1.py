import wpf
import os
import re
import pylev
from itertools import ifilter

from System.Windows import Application, Window
from System import Uri
from System.Windows.Media.Imaging import BitmapImage, BitmapCreateOptions,BitmapCacheOption

mov_types = ['.avi', '.wmv', '.mkv', '.mp4']
folder_filter = lambda file: os.path.splitext(file)[1] == '.jpg'
mov_filter = lambda file: any(os.path.splitext(file)[1] == mov_type for mov_type in mov_types)

class MyWindow(Window):
    def __init__(self):
        wpf.LoadComponent(self, 'WpfApplication1.xaml')
        self.itor = self.traverseDir('d:/')
        self.setImage(self.itor.next())

    def traverseDir(self, root):
        for dirName, subdirList, fileList in os.walk(root):
            mov = next((x for x in fileList if any(os.path.splitext(x)[1] == mov_type for mov_type in mov_types)), None)
            self.mov.Text = mov
            if mov is None:
                continue
            if any(filter(lambda file: file == 'folder.jpg', fileList)):
                 continue
            #ifilter(lambda t: all(f(t) for f in [folder_filter, mov_filter]), fileList)
            _fileList = filter(lambda file: os.path.splitext(file)[1] == '.jpg', fileList)
            fildDict = {k: pylev.levenschtein(k, mov) for k in _fileList }
            _fileList = sorted(fildDict, key=fildDict.__getitem__)
            self.lv.Items.Clear()
            self.loc.Text = dirName
            map(lambda x: self.lv.Items.Add(x) , _fileList)    
            for fname in _fileList:
                finished = yield '%s/%s' % (dirName, fname)
                if finished:
                    break

    def setImage(self, path):
        self.txt.Text = path
        try:
            image = BitmapImage()
            image.BeginInit();
            image.CacheOption = BitmapCacheOption.OnLoad;
            image.CreateOptions = BitmapCreateOptions.IgnoreImageCache;
            image.UriSource = Uri(path);
            image.EndInit();
            self.img.Source = image
        except:
            pass
               
    def Next_Click(self, sender, e): # next button
        path = self.itor.send(False)
        self.setImage(path)
        
    def OK_Click(self, sender, e): # ok button
        path = self.itor.send(True)
        oldpath = self.txt.Text
        self.setImage(path)
        #self.sts.Text = oldpath
        try:
            os.rename(oldpath, os.path.join(os.path.dirname(oldpath), 'folder.jpg'))
        except:
            pass

    def Skip_Click(self, sender, e): # ok button
        path = self.itor.send(True)
        self.setImage(path)
    
    def lv_SelectionChanged(self, sender, e):
        pass

if __name__ == '__main__':
    Application().Run(MyWindow())
