class Project:
    def __init__(self):
        # TODO: Need to populate these
        # self.processedList = None
        # self.notRatedList = None
        # self.interpolateList = None
        # self.dataFolder = None
        # self.params = None
        # self.mask = ext
        # self.nSubject = None
        # self.nBlock = None
        # self.resultFolder = None
        # self.nProcessedFiles = None
        # self.CGV = None

    def getRatedCount(self):
        return len(self.processedList) -\
        (len(self.notRatedList) + len(self.interpolateList))

    def toBeInterpolatedCount(self):
        return len(self.interpolateList)

    def areFoldersChanged(self):
        # TODO: Implement isFolderChanged
        dataChanged = self.isFolderChanged(self.dataFolder,
        self.nSubject, self.nBlock, self.mask, self.params.Settings.trackAllSteps);
        resultChanged = self.isFolderChanged(self.resultFolder, ...
        [], self.nProcessedFiles, self.CGV.EXTENSIONS(1).mat, self.params.Settings.trackAllSteps);
        return dataChanged | | resultChanged;
