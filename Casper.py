import math


class Casper:
    def __init__(self, totalD, h, baseInterestFactor, basePenaltyFactor, baseDepositDependence, attackDuration,
                 exponentialTerm=0):
        self.INITIAL_SCALE_FACTOR = 10000000000

        self.validatorInitDeposits = [0, 0, ]
        self.validatorPrevDeposits = [0, 0]
        self.validatorDeposits = [0, 0]
        #  We consider two validators, one is attacked, other is not. -> 한명은 censorship 당해서 투표 안함 처리되고 한명은 투표한걸로 처리
        #0 = attacker, 1 = victim
        self.numValidators = 2

        self.baseInterestFactor = baseInterestFactor
        self.basePenaltyFactor = basePenaltyFactor
        self.baseDepositDependence = baseDepositDependence

        self.rewardFactor = self.baseInterestFactor / \
                            math.pow(totalD, baseDepositDependence)
        self.depositScaleFactor = self.INITIAL_SCALE_FACTOR
        self.prevDepositScaleFactor = self.depositScaleFactor

        self.totalVoteUnscaled = 0
        self.epoch = 0
        # we assume that when we begin, the previous two epochs were justified
        self.lastJustifiedEpoch = 0
        self.lastFinalizedEpoch = -1
        self.finalizationEpoch = 0

        self.D = totalD
        # h is the deposit fraction of the validator who is being 'censored'.
        # During a censorship attack self validator represents the victims,
        # during a minority fork those who are voting on the other chain
        self.h = h
        self.attackDuration = attackDuration
        self.exponentialTerm = math.inf
        if (exponentialTerm > 0):
            self.exponentialTerm = exponentialTerm

        self.initValidators(totalD, h)

    def initValidators(self, D, h):
        self.validatorDeposits[0] = D * (1 - h) / self.INITIAL_SCALE_FACTOR
        self.validatorDeposits[1] = D * h / self.INITIAL_SCALE_FACTOR
        for i in range(0, self.numValidators):
            self.validatorPrevDeposits[i] = self.validatorDeposits[i]
            self.validatorInitDeposits[i] = self.validatorDeposits[i]

    def getTotalDepositsUnscaled(self, ):
        result = 0
        for i in range(0, self.numValidators):
            result += self.validatorDeposits[i]
        return result

    def getESF(self, ):
        return self.epoch - self.lastFinalizedEpoch

    def getCollectiveReward(self, ):
        # relevant for the first epoch, as we are assuming that we start in something close to steady-state
        if (self.epoch == 1):
            return self.rewardFactor / 2  # 왜 epoch = 1 이면 투표율 고려안하지??

        votePercentage = self.totalVoteUnscaled / self.getTotalDepositsUnscaled()

        if (self.getESF() > 2):
            votePercentage = 0

        return votePercentage * self.rewardFactor / 2

    def getScaledDeposit(self, i):
        # We consider the deposits _after_ the rescale. Since we process the whole epoch in a single call to processEpoch,
        # self is equivalent to multiplying the base deposits at the start of the previous epoch with the current scale factor.
        return self.validatorPrevDeposits[i] * self.depositScaleFactor

    def getNextScaledDeposit(self, i):
        return self.validatorDeposits[i] * self.depositScaleFactor

    def getFinalizationEpoch(self, ):
        if (self.getESF() == 1):
            return self.finalizationEpoch
        else:
            return "not finalized"

    def processEpoch(self, ):
        self.epoch += 1
        for i in range(0, self.numValidators):
            self.validatorPrevDeposits[i] = self.validatorDeposits[i]

        # update scale factor
        self.prevDepositScaleFactor = self.depositScaleFactor
        if (self.epoch > 1):
            self.depositScaleFactor = self.depositScaleFactor * \
                                      (1 + self.getCollectiveReward()) / (1 + self.rewardFactor)

        # update reward factor
        self.rewardFactor = self.baseInterestFactor / math.pow(self.getTotalDepositsUnscaled(
        ) * self.prevDepositScaleFactor, self.baseDepositDependence) + self.basePenaltyFactor * (self.getESF() - 2)
        if (self.getESF() >= self.exponentialTerm):
            self.rewardFactor += (math.exp(self.getESF() - self.exponentialTerm) - 1) * self.basePenaltyFactor

        # update base deposits
        self.totalVoteUnscaled = 0

        for i in range(0, self.numValidators):
            if ((i == 0) or (self.epoch > self.attackDuration)):
                self.validatorDeposits[i] += self.validatorDeposits[i] * \
                                             self.rewardFactor
                self.totalVoteUnscaled += self.validatorDeposits[i]

            # check for justification/finalization
            if (
                    self.totalVoteUnscaled / self.getTotalDepositsUnscaled() > 2 / 3 and self.lastJustifiedEpoch < self.epoch):
                if (self.lastJustifiedEpoch == self.epoch - 1):
                    if (self.epoch - self.lastFinalizedEpoch >= 3):
                        self.finalizationEpoch = self.epoch  # just for tracing purposes
                    self.lastFinalizedEpoch = self.epoch - 1

                self.lastJustifiedEpoch = self.epoch


    def getDepositChange(self, idx):
        return (self.getScaledDeposit(idx) / self.INITIAL_SCALE_FACTOR) / self.validatorInitDeposits[idx] - 1

    # 아무데도 안쓰이는 함수
    def processEpochs(self, n):
        deps = []
        z = self.numValidators - 1

        for i in range(0, n):
            self.processEpoch()
            if (i % (math.ceil(n / 1000)) == 0):
                depsDepn = math.pow(
                    self.numValidators * self.validatorInitDeposits[z] * self.INITIAL_SCALE_FACTOR,
                    self.baseDepositDependence)
                interest = math.pow(
                    1 + self.f * self.baseInterestFactor / (2 * depsDepn), i)
                naiveDep = self.validatorInitDeposits[z] * \
                           self.INITIAL_SCALE_FACTOR * interest
                deps.append(i + ", " + self.getScaledDeposit(z) + " " +
                            naiveDep + " " + (self.getScaledDeposit(z) / naiveDep))
        return deps
