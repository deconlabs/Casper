import numpy as np
import matplotlib.pyplot as plt

from Casper import Casper


# 3a 와 3b 의 차이는 p=0, p=1
# 각각의 figure 안에는 공격없을 때 시나리오와 공격있을때 시나리오(Casper 클래스)가 들어있다
# 의문점은 공격없을때 시나리오에도 공격받는 validator 와 공격받지 않는 validator 로 나뉘어있는데 이게 뭐하는건지 모르겠다.

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

    deposit_change = []
    for j in range(0, maxEpochs):

        casperHonest.processEpoch()
        casperAttack.processEpoch()
        if (overtake == -1 and (casperHonest.getScaledDeposit(0) < casperAttack.getScaledDeposit(0))):
            overtake = j
            Dovertake = casperHonest.getScaledDeposit(0)

        if (j > traceCounter * traceEpochStep):
            traceCounter += 1
            honest_deposit_change = casperHonest.getDepositChange(0)
            attack_deposit_change = casperAttack.getDepositChange(0)
            deposit_change.append((honest_deposit_change, attack_deposit_change))

            atext = ",".join(map(str, [j, tau, h,honest_deposit_change ,attack_deposit_change , casperAttack.getDepositChange(1)]))
            print(atext)
            text += "\n" + atext


    deposit_change = np.array(deposit_change)
    plt.plot(deposit_change[:,0],color='r')
    plt.plot(deposit_change[:,1],color='b')
    plt.xlabel("epoch i")
    plt.ylabel("Reserve Received ")
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

    deposit_change = []
    for j in range(0, maxEpochs):

        casperHonest.processEpoch()
        casperAttack.processEpoch()
        if (overtake == -1 and (casperHonest.getScaledDeposit(0) < casperAttack.getScaledDeposit(0))):
            overtake = j
            Dovertake = casperHonest.getScaledDeposit(0)

        if (j > traceCounter * traceEpochStep):
            traceCounter += 1
            honest_deposit_change = casperHonest.getDepositChange(0)
            attack_deposit_change = casperAttack.getDepositChange(0)
            deposit_change.append((honest_deposit_change, attack_deposit_change))

            atext = ",".join(
                map(str, [j, tau, h, honest_deposit_change, attack_deposit_change, casperAttack.getDepositChange(1)]))
            print(atext)
            text += "\n" + atext

    deposit_change = np.array(deposit_change)
    plt.plot(deposit_change[:, 0],color='r')
    plt.plot(deposit_change[:, 1],color='b')
    plt.xlabel("epoch i")
    plt.ylabel("Reserve Received ")
    plt.title(" p = 1 ")
    plt.savefig("Fig3b")
    plt.close()
    # fileContents = document.getElementById('filecontents')
    # fileContents.innerText = text





def doExperimentFigure4a():
    h = 0.00001
    startH = 0.3
    stepH = 0.001
    endH = 1.0
    baseMaxEpochs = 100000

    text = "h,first_finalization_epoch"
    h_list = []
    FinalizationEpoch = []

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
        final_epoch = casper.getFinalizationEpoch()
        FinalizationEpoch.append(final_epoch)
        h_list.append(h)
        atext = str(h) + "," + str(final_epoch)
        print(atext)
        text += "\n" + atext

    h_list = np.array(h_list)
    plt.plot((1 - h_list)[::-1], np.array(FinalizationEpoch))
    plt.xlabel("alpha")
    plt.ylabel("first finalization epoch")
    plt.title("Benchmark setting")
    plt.ylim(-1000, 10000)
    plt.savefig("Fig4a")

    # fileContents = document.getElementById('filecontents')
    # fileContents.innerText = text


def doExperimentFigure4b():
    h = 0.00001
    startH = 0.3
    stepH = 0.001
    endH = 1.0
    baseMaxEpochs = 100000

    text = "h,first_finalization_epoch"

    FinalizationEpoch = []
    h_list = []
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
        final_epoch = casper.getFinalizationEpoch()
        FinalizationEpoch.append(final_epoch)
        h_list.append(h)

        atext = str(h) + "," + str(final_epoch)
        print(atext)
        text += "\n" + atext

    # fileContents = document.getElementById('filecontents')
    # fileContents.innerText = text
    h_list = np.array(h_list)
    plt.plot((1 - h_list)[::-1], np.array(FinalizationEpoch))
    plt.xlabel("alpha")
    plt.ylabel("first finalization epoch")
    plt.title("added exponential term")
    plt.ylim(-1000, 10000)
    plt.savefig("Fig4b")


doExperimentFigure3a()
doExperimentFigure3b()
# doExperimentFigure4a()
# doExperimentFigure4b()
