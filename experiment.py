import matplotlib.pyplot as plt
import numpy as np

from Casper import Casper


#3a 와 3b 의 차이는 p=0, p=1
#각각의 figure 안에는 공격없을 때 시나리오와 공격있을때 시나리오(Casper 클래스)가 들어있다

#의문점은 공격없을때 시나리오에도 공격받는 validator 와 공격받지 않는 validator 로 나뉘어있는데 이게 뭐하는건지 모르겠다.

def doExperimentFigure3a():
    tau = 2000
    traceEpochStep = 100
    traceCounter = 0
    h = 0.25  # victim's stake

    text = "j,tau,h,D_normal,D_noncensored,D_censored"
    n = 2
    totalD = 100000
    baseDepositDependence = 0  # p
    baseInterestFactor = 0.00017  # gamma
    basePenaltyFactor = 0.0000002  # beta


    # tau = 0 이면 공격이 없는 것 -> 모두가 honest 한 casperHonest
    casperHonest = Casper(totalD, h, baseInterestFactor,
                          basePenaltyFactor, baseDepositDependence, 0)
    casperAttack = Casper(totalD, h, baseInterestFactor,
                          basePenaltyFactor, baseDepositDependence, tau)
    overtake = -1
    maxEpochs = 7002

    storage_depositscaleF = []
    for j in range(0, maxEpochs):

        depositscaleF = casperHonest.processEpoch()
        # storage_depositscaleF.append(depositscaleF)
        casperAttack.processEpoch()
        if (overtake == -1 and (casperHonest.getScaledDeposit(0) < casperAttack.getScaledDeposit(0))):
            overtake = j
            Dovertake = casperHonest.getScaledDeposit(0)

        if (j > traceCounter * traceEpochStep):
            traceCounter += 1

            atext = ",".join(map(str, [j, tau, h, casperHonest.getDepositChange(
                0), casperAttack.getDepositChange(0), casperAttack.getDepositChange(1)]))
            print(atext)
            text += "\n" + atext

    casperAttack_deposit = np.array(casperAttack.validatorDeposits)
    casperHonest_deposit = np.array(casperHonest.validatorDeposits)

    totalD = casperAttack_deposit + casperHonest_deposit
    plt.plot(casperHonest_deposit / totalD)
    plt.plot(casperAttack_deposit / totalD)
    plt.xlabel("epoch i")
    plt.ylabel("Deposit share")
    plt.title(" p = 0 ")
    plt.savefig("Fig3a")
    plt.close()
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

    casperHonest = Casper(totalD, h, baseInterestFactor,
                          basePenaltyFactor, baseDepositDependence, 0)
    casperAttack = Casper(totalD, h, baseInterestFactor,
                          basePenaltyFactor, baseDepositDependence, tau)
    overtake = -1
    maxEpochs = 7002

    for j in range(0, maxEpochs):
        casperHonest.processEpoch()
        casperAttack.processEpoch()
        if (overtake == -1 and (casperHonest.getScaledDeposit(0) < casperAttack.getScaledDeposit(0))):
            overtake = j
            Dovertake = casperHonest.getScaledDeposit(0)

        if (j > traceCounter * traceEpochStep):
            traceCounter += 1
            atext = ",".join(map(str, [j, tau, h, casperHonest.getDepositChange(
                0), casperAttack.getDepositChange(0), casperAttack.getDepositChange(1)]))
            print(atext)
            text += "\n" + atext

    casperAttack_deposit = np.array(casperAttack.validatorDeposits)  # attack 이 있을 때 [honest , attacker ] deposit
    casperHonest_deposit = np.array(casperHonest.validatorDeposits)

    totalD = casperAttack_deposit + casperHonest_deposit
    plt.plot(casperHonest_deposit / totalD)
    plt.plot(casperAttack_deposit / totalD)
    plt.xlabel("epoch i")
    plt.ylabel("Deposit share")
    plt.title(" p = 1 ")
    plt.savefig("Fig3b")
    plt.close()
    # fileContents = document.getElementById('filecontents')
    # fileContents.innerText = text

import numpy as np
def doExperimentFigure4a():
    h = 0.00001
    startH = 0.3
    stepH = 0.001
    endH = 1.0
    baseMaxEpochs = 100000

    text = "h,first_finalization_epoch"

    for h in np.arange(startH, endH, stepH):

        n = 2
        eachValidatorD = 10000000
        baseInterestFactor = 0.007
        basePenaltyFactor = 0.0000002
        baseDepositDependence = 0.5
        maxEpochs = baseMaxEpochs

        casper = Casper(eachValidatorD, h, baseInterestFactor,
                        basePenaltyFactor, baseDepositDependence, maxEpochs, 0)

        for j in range(0, maxEpochs):
            casper.processEpoch()
            if (casper.lastFinalizedEpoch > -1):
                break

        atext = str(h) + "," + str(casper.getFinalizationEpoch())
        print(atext)
        text += "\n" + atext
    print(atext)
    # fileContents = document.getElementById('filecontents')
    # fileContents.innerText = text


def doExperimentFigure4b():
    h = 0.00001
    startH = 0.3
    stepH = 0.001
    endH = 1.0
    baseMaxEpochs = 100000

    text = "h,first_finalization_epoch"

    for h in np.arange(startH, endH, stepH):
        n = 2
        eachValidatorD = 10000000
        baseInterestFactor = 0.007
        basePenaltyFactor = 0.0000002
        baseDepositDependence = 0.5

        maxEpochs = baseMaxEpochs
        casper = Casper(eachValidatorD, h, baseInterestFactor,
                        basePenaltyFactor, baseDepositDependence, maxEpochs, 1000)
        for j in range(0, maxEpochs):
            casper.processEpoch()
            if (casper.lastFinalizedEpoch > -1):
                break

        atext = str(h) + "," + str(casper.getFinalizationEpoch())
        print(atext)
        text += "\n" + atext

    # fileContents = document.getElementById('filecontents')
    # fileContents.innerText = text


#doExperimentFigure3a()
# doExperimentFigure3b()
doExperimentFigure4a()
# doExperimentFigure4b()
