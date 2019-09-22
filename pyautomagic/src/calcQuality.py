def calcQuality(Dat,bad_chans,overallThresh=50,timeThresh=25,chanThresh=25,avRef=True):
    """ Calculates four essential quality metrics of a data set
    INPUTS: Dat, a channels x timepoints data array of EEG
            bad_chans, a list of the numbers of bad channels
            overallThresh, timeThresh, and chanThresh are thresholds for 3 of the metrics
            avRef, boolean for if average referencing should be applied
    OUTPUTS: quality_metrics, a dictionary of the quality metrics and thresholds/settings used
    The four quality metrics:
        Overall high amplitude data points
        Timepoints of high variance across channels
        Ratio of bad channels
        Channels of high variance across time
        
        Mean absolute voltage also calculated
    """
    import numpy as np
    #checking all of the default value types, if not what they should be, use default
    if not isinstance(overallThresh,int) and not isinstance(overallThresh,float):
        overallThresh = 50
        print('Invalid overallThresh value. Default of 50 used.')
    if not isinstance(timeThresh,int) and not isinstance(timeThresh,float):
        timeThresh = 25
        print('Invalid timeThresh value. Default of 25 used.')
    if not isinstance(chanThresh,int) and not isinstance(chanThresh,float):
        chanThresh = 25
        print('Invalid chanThresh value. Default of 25 used.')
    if not isinstance(avRef,bool):
        # ADD STATEMENT TO ALLOW TYPICAL OTHER BOOLEAN INDICATORS
        avRef = True
        print('Invalid avRef value. Average referencing used.')
    # ADD CHECKS FOR DAT AND BAD_CHANS?
        
    dimensions = np.shape(Dat)#tuple of EEG data info
    n_chans = dimensions[0]
    n_timepts = dimensions[1]
    n_elements = dimensions[0]*dimensions[1]#total number data points
    # perform average reference
    if avRef:
        av = np.mean(Dat,0)
        Dat = Dat - np.tile(av,(n_chans,1))
    # Calculating quality metrics
    # Overall high amplitude data points
    OHA = np.sum(np.absolute(Dat)>overallThresh)/n_elements
    # Timepoints of high variance
    std_across_chans = np.std(Dat,0)
    THV = np.sum(std_across_chans>timeThresh)/n_timepts
    # Ratio of bad channels
    RBC = len(bad_chans)/n_chans
    # Channels of high variance
    std_across_time = np.std(Dat,1)
    CHV = np.sum(std_across_time>chanThresh)/n_chans
    # unthresholded mean absolute voltage
    MAV = np.mean(np.absolute(Dat))
    quality_metrics = {'OHA':OHA,'THV':THV,'RBC':RBC,'CHV':CHV,'MAV':MAV,#actual results
                       'ot':overallThresh,'tt':timeThresh,'ct':chanThresh,'ar':avRef}#for development
    return quality_metrics

