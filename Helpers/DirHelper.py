import os

class DirHelper:

    @staticmethod
    def CreateDir(path):
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def CleanDir(path):
        for (dirpath, dirnames, filenames) in os.walk(path):
            for filename in filenames:
                os.remove(os.sep.join([dirpath, filename]))