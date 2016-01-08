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
            mov = next((x for x in fileList if any(os.path.splitext(x)[1] == mov_type for mov_type in mov_types)), None) # 2 and more?
            self.mov.Text = mov
            if mov is None:
                continue
            if any(filter(lambda file: file == 'folder.jpg', fileList)):
                 continue
            #ifilter(lambda t: all(f(t) for f in [folder_filter, mov_filter]), fileList)
            _fileList = filter(lambda file: os.path.splitext(file)[1] == '.jpg', fileList)

            if _fileList == [] :
                continue
            fileDict = {k: pylev.levenschtein(k, mov) for k in _fileList }
            _fileList = sorted(fileDict, key=fileDict.__getitem__)
            self.lv.Items.Clear()
            self.loc.Text = dirName
            map(lambda x: self.lv.Items.Add(x) , _fileList)    
            finished = yield '%s/%s' % (dirName, _fileList[0])

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

    def OK_Click(self, sender, e): # ok button
        try:       
            oldpath = self.txt.Text
            os.rename(self.selectFile, os.path.join(os.path.dirname(self.selectFile), 'folder.jpg'))
        except:
            pass

        try:
            path = self.itor.send(True)
            self.setImage(path)
        except StopIteration:
            Application.Current.Shutdown()


    def Skip_Click(self, sender, e): # skip button
        try:
            path = self.itor.send(True)
        except StopIteration:
            Application.Current.Shutdown()
        self.setImage(path)
    
    def lv_SelectionChanged(self, sender, e):
        if sender.SelectedItem != None:
            self.sts.Text = "item selected : " + sender.SelectedItem
            self.selectFile = self.loc.Text + "/" + sender.SelectedItem
            self.setImage(self.selectFile)
    
if __name__ == '__main__':
    Application().Run(MyWindow())
