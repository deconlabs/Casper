from Casper import Casper

def doExperimentFigure3a():
    tau = 2000
    traceEpochStep = 100
    traceCounter = 0
    h = 0.25 # victim's stake
    
    text = "j,tau,h,D_normal,D_noncensored,D_censored"
    n = 2
    totalD = 100000
    baseDepositDependence = 0 # p 
    baseInterestFactor = 0.00017 # gamma
    basePenaltyFactor = 0.0000002 # beta 

    casperHonest = Casper(totalD, h, baseInterestFactor, basePenaltyFactor, baseDepositDependence, 0)
    casperAttack = Casper(totalD, h, baseInterestFactor, basePenaltyFactor, baseDepositDependence, tau)
    overtake = -1
    maxEpochs = 7002
    
    for j in range(0, maxEpochs):
    
        casperHonest.processEpoch()
        casperAttack.processEpoch()
        if(overtake == -1 and (casperHonest.getScaledDeposit(0) < casperAttack.getScaledDeposit(0))):
            overtake = j
            Dovertake = casperHonest.getScaledDeposit(0)
        
        if(j > traceCounter*traceEpochStep):
            traceCounter+=1

            atext = ",".join(map(str, [j,tau,h,casperHonest.getDepositChange(0),casperAttack.getDepositChange(0),casperAttack.getDepositChange(1)]))
            print(atext)
            text += "\n"+atext
        
    # fileContents = document.getElementById('filecontents') 
    # fileContents.innerText = text 


def doExperimentFigure3b():
    tau = 2000
    traceEpochStep = 100
    traceCounter = 0
    h = 0.25
    
    text = "j,tau,h,D_normal,D_noncensored,D_censored"
    n = 2
    totalD = 100000
    baseDepositDependence = 1
    baseInterestFactor = 20.
    basePenaltyFactor = 0.0000002

    casperHonest = Casper(totalD, h, baseInterestFactor, basePenaltyFactor, baseDepositDependence, 0)
    casperAttack = Casper(totalD, h, baseInterestFactor, basePenaltyFactor, baseDepositDependence, tau)
    overtake = -1
    maxEpochs = 7002
    
    for j in range(0, maxEpochs):
        casperHonest.processEpoch()
        casperAttack.processEpoch()
        if(overtake == -1 and (casperHonest.getScaledDeposit(0) < casperAttack.getScaledDeposit(0))):
            overtake = j
            Dovertake = casperHonest.getScaledDeposit(0)
        
        if(j > traceCounter*traceEpochStep):
            traceCounter+=1
            atext = ",".join(map(str, [j,tau,h,casperHonest.getDepositChange(0),casperAttack.getDepositChange(0),casperAttack.getDepositChange(1)]))
            print(atext)
            text += "\n"+atext
        

    
    # fileContents = document.getElementById('filecontents') 
    # fileContents.innerText = text 


def doExperimentFigure4a():
    h = 0.00001
    startH = 0.3
    stepH = 0.001
    endH = 1.0
    baseMaxEpochs = 100000
    
    text = "h,first_finalization_epoch"

    for h in range(startH , endH, stepH):
    
        n = 2
        eachValidatorD = 10000000
        baseInterestFactor = 0.007
        basePenaltyFactor = 0.0000002
        baseDepositDependence = 0.5

        casper = Casper(eachValidatorD, h, baseInterestFactor, basePenaltyFactor, baseDepositDependence, maxEpochs, 0)
        maxEpochs = baseMaxEpochs

        for j in range(0, maxEpochs):
            casper.processEpoch()
            if(casper.lastFinalizedEpoch > -1): 
                break
        
        atext = str(h)+","+str(casper.getFinalizationEpoch())
        print(atext)
        text += "\n"+atext

    
    # fileContents = document.getElementById('filecontents') 
    # fileContents.innerText = text 

def doExperimentFigure4b():
    h = 0.00001
    startH = 0.3
    stepH = 0.001
    endH = 1.0
    baseMaxEpochs = 100000
    
    text = "h,first_finalization_epoch"

    for h in range(startH, endH, stepH):
        n = 2
        eachValidatorD = 10000000
        baseInterestFactor = 0.007
        basePenaltyFactor = 0.0000002
        baseDepositDependence = 0.5

        casper = Casper(eachValidatorD, h, baseInterestFactor, basePenaltyFactor, baseDepositDependence, maxEpochs, 1000)
        maxEpochs = baseMaxEpochs
        for j in range(0, maxEpochs):
            casper.processEpoch()
            if(casper.lastFinalizedEpoch > -1):
                break
            
            
        atext = str(h)+","+str(casper.getFinalizationEpoch())
        print(atext)
        text += "\n"+atext
    
    # fileContents = document.getElementById('filecontents') 
    # fileContents.innerText = text 


# doExperimentFigure3a()
doExperimentFigure3b()
# doExperimentFigure4a()
# doExperimentFigure4b()
