def rateQuality(OHA, THV, CHV, RCB, overallGoodCutoff=0.1, overallBadCutoff=0.2, timeGoodCutoff=0.1, timeBadCutoff=0.2,
                channelGoodCutoff=0.15, channelBadCutoff=0.3, BadChannelGoodCutoff=0.15, BadChannelBadCutoff=0.3):

    # Program verifies that the values are Numeric Type, if not, uses the default values
    if not isinstance(overallGoodCutoff, int) and not isinstance(overallGoodCutoff, float):
        overallGoodCutoff = 0.1
        print('Error: overallGoodCutoff invalid value, using default')
    if not isinstance(overallBadCutoff, int) and not isinstance(overallBadCutoff, float):
        overallBadCutoff = 0.2
        print('Error: overallBadCutoff invalid value, using default')

    if not isinstance(timeGoodCutoff, int) and not isinstance(timeGoodCutoff, float):
        timeGoodCutoff = 0.1
        print('Error: timeGoodCutoff invalid value, using default')
    if not isinstance(timeBadCutoff, int) and not isinstance(timeBadCutoff, float):
        timeBadCutoff = 0.2
        print('Error: timeBadCutoff invalid value, using default')

    if not isinstance(channelGoodCutoff, int) and not isinstance(channelGoodCutoff, float):
        channelGoodCutoff = 0.15
        print('Error: channelGoodCutoff invalid value, using defult')
    if not isinstance(channelBadCutoff, int) and not isinstance(channelBadCutoff, float):
        channelBadCutoff = 0.3
        print('Error: channelBadCutoff invalid value, using default')

    if not isinstance(BadChannelGoodCutoff, int) and not isinstance(BadChannelGoodCutoff, float):
        BadChannelGoodCutoff = 0.15
        print('Error: BadChannelGoodCutoff invalid value, using default')
    if not isinstance(BadChannelBadCutoff, int) and not isinstance(BadChannelBadCutoff, float):
        BadChannelBadCutoff = 0.3
        print('Error: BadChannelBadCutoff invalid value, using default')

    if not isinstance(OHA, str) and not isinstance(THV, str) and not isinstance(CHV, str):
        qualityScores = [OHA, THV, CHV]
        print('Error: No qualityScores found, using defaults')

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
