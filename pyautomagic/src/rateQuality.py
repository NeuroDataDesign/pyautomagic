def rateQuality(OHA, THV, CHV, RCB, overallGoodCutoff:float=0.1, overallBadCutoff:float=0.2, timeGoodCutoff:float=0.1, timeBadCutoff:float=0.2,
                channelGoodCutoff:float=0.15, channelBadCutoff:float=0.3, BadChannelGoodCutoff:float=0.15, BadChannelBadCutoff:float=0.3):
    
    # check that thresholds are between 0 and 1
    if any(isinstance(x, int) for x in [fill_this_in]) or any(x <= 0 or x >= 1 for x in [fill_this_in]):
           logger.log(f"Some threshold cutoffs were set as integer. Please pass in a float between 0 and 1. You passed in {stuff}."
           raise ValueError("Say something")

    qualityScores = [OHA, THV, CHV, RCB]
    Qs = qualityScores

    # Categorize wrt OHA
    if Qs[0] < overallGoodCutoff:
        OHA = 'Good'
    elif overallGoodCutoff <= Qs[0] < overallBadCutoff:
        OHA = 'Ok'
    else:
        OHA = 'Bad'

    # Categorize wrt THV
    if Qs[1] < timeGoodCutoff:
        THV = 'Good'
    elif timeGoodCutoff <= Qs[1] < timeBadCutoff:
        THV = 'Ok'
    else:
        THV = 'Bad'

    # Categorize wrt CHV
    if Qs[2] < channelGoodCutoff:
        CHV = 'Good'
    elif channelGoodCutoff <= Qs[2] < channelBadCutoff:
        CHV = 'Ok'
    else:
        CHV = 'Bad'

    # Categorize wrt RBC
    if Qs[3] < BadChannelGoodCutoff:
        RCB = 'Good'
    elif BadChannelGoodCutoff <= Qs[3] < BadChannelBadCutoff:
        RCB = 'Ok'
    else:
        RCB = 'Bad'

    if OHA == ' Bad ' or THV == ' Bad ' or CHV == ' Bad ' or RCB == ' Bad ':
        print('Bad Rating')

    if OHA == ' Ok ' or THV == ' Ok ' or CHV == ' Ok ' or RCB == ' Ok ':
        print('Ok Rating')

    if OHA == ' Good ' or THV == ' Good ' or CHV == ' Good ' or RCB == ' Good ':
        print('Good Rating')
