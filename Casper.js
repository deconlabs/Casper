class Casper {
	constructor(totalD, h, baseInterestFactor, basePenaltyFactor, baseDepositDependence, attackDuration, exponentialTerm=0) {
        this.validatorInitDeposits = [];
        this.validatorPrevDeposits = [];
        this.validatorDeposits = [];
        // We consider two validators, one is attacked, other is not.
        this.numValidators = 2;

        this.baseInterestFactor = baseInterestFactor;
        this.basePenaltyFactor = basePenaltyFactor;
        this.baseDepositDependence = baseDepositDependence;

        this.rewardFactor = this.baseInterestFactor/Math.pow(totalD, baseDepositDependence); 
        this.depositScaleFactor = Casper.INITIAL_SCALE_FACTOR; // 이게 무슨 문법이다냐
        this.prevDepositScaleFactor = this.depositScaleFactor;

        this.totalVoteUnscaled = 0;
        this.epoch = 0;
        // we assume that when we begin, the previous two epochs were justified
        this.lastJustifiedEpoch = 0;
        this.lastFinalizedEpoch = -1;
        this.finalizationEpoch = 0;
        
        this.D = totalD;
        // h is the deposit fraction of the validator who is being 'censored'. During a censorship attack this validator represents the victims, during a minority fork those who are voting on the other chain
        this.h = h;
        this.attackDuration = attackDuration;
        this.exponentialTerm = Number.POSITIVE_INFINITY;
        if(exponentialTerm > 0) this.exponentialTerm = exponentialTerm;
        
        this.initValidators(totalD, h);
	}
	
	initValidators(D, h) {
        this.validatorDeposits[0] = D*(1-h) / Casper.INITIAL_SCALE_FACTOR;
        this.validatorDeposits[1] = D*h / Casper.INITIAL_SCALE_FACTOR;
		for(var i=0; i<this.numValidators; i++) {
			this.validatorPrevDeposits[i] = this.validatorDeposits[i];
            this.validatorInitDeposits[i] = this.validatorDeposits[i];
		}
	}
	
	getTotalDepositsUnscaled() {
		var result = 0;
		for(var i=0;i<this.numValidators;i++) {
			result += this.validatorDeposits[i];
		}
		return result;
	}
    
    getESF() {
        return this.epoch - this.lastFinalizedEpoch;
    }
    
    getCollectiveReward() {
        // relevant for the first epoch, as we are assuming that we start in something close to steady-state
        if(this.epoch == 1) return this.rewardFactor/2;
        var votePercentage = this.totalVoteUnscaled/this.getTotalDepositsUnscaled();
		if(this.getESF() > 2) votePercentage = 0;
        return votePercentage*this.rewardFactor/2; // m * ro/2
    }
    
    getScaledDeposit(i) {
        // We consider the deposits _after_ the rescale. Since we process the whole epoch in a single call to processEpoch,
        // this is equivalent to multiplying the base deposits at the start of the previous epoch with the current scale factor.
        return this.validatorPrevDeposits[i] * this.depositScaleFactor;
    }
    
    getNextScaledDeposit(i) {
        return this.validatorDeposits[i] * this.depositScaleFactor;
    }
    
    getFinalizationEpoch() {
        if(this.getESF() == 1) return this.finalizationEpoch;
        else return "not finalized";
    }
	
	processEpoch() {
		this.epoch++;
		for(var i=0; i<this.numValidators; i++) {
			this.validatorPrevDeposits[i] = this.validatorDeposits[i];
		}
		
		// update scale factor
        this.prevDepositScaleFactor = this.depositScaleFactor;
		if(this.epoch > 1) this.depositScaleFactor = this.depositScaleFactor * (1 + this.getCollectiveReward())/(1 + this.rewardFactor);
		
		// update reward factor
		this.rewardFactor = this.baseInterestFactor/Math.pow(this.getTotalDepositsUnscaled() * this.prevDepositScaleFactor, this.baseDepositDependence) + this.basePenaltyFactor * (this.getESF()-2); 
		if(this.getESF() >= this.exponentialTerm) this.rewardFactor += (Math.exp(this.getESF()-this.exponentialTerm) - 1) * this.basePenaltyFactor;
        
        // update base deposits
    
		this.totalVoteUnscaled = 0;
		for(var i=0; i<this.numValidators; i++) {
			if((i == 0) || (this.epoch > this.attackDuration)) {
				this.validatorDeposits[i] += this.validatorDeposits[i] * this.rewardFactor;
				this.totalVoteUnscaled += this.validatorDeposits[i];
			}
            // check for justification/finalization
            if(this.totalVoteUnscaled/this.getTotalDepositsUnscaled() > 2./3 && this.lastJustifiedEpoch < this.epoch) {
                if(this.lastJustifiedEpoch == this.epoch-1) {
                    if(this.epoch - this.lastFinalizedEpoch >= 3) this.finalizationEpoch = this.epoch; // just for tracing purposes
                    this.lastFinalizedEpoch = this.epoch-1;
                }
                this.lastJustifiedEpoch = this.epoch;
            }
		}
	}
    
    getDepositChange(idx) {
        return (this.getScaledDeposit(idx)/Casper.INITIAL_SCALE_FACTOR)/this.validatorInitDeposits[idx] - 1;
    }
    
    processEpochs(n) { // 이건 뭐하는 함수인지 모르겠네
        var deps = [];
        var z = this.numValidators - 1;
        for(var i=0;i<n;i++) {
            this.processEpoch();
            if(i%(Math.ceil(n/1000))==0) {
                var depsDepn = Math.pow(this.numValidators*this.validatorInitDeposits[z]*Casper.INITIAL_SCALE_FACTOR, this.baseDepositDependence);
                var interest = Math.pow(1+this.f*this.baseInterestFactor/(2*depsDepn), i);
                var naiveDep = this.validatorInitDeposits[z]*Casper.INITIAL_SCALE_FACTOR*interest;
                deps.push(i+", "+this.getScaledDeposit(z)+" "+naiveDep+" "+(this.getScaledDeposit(z)/naiveDep));
            }
        }
        return deps;
    }
}

Casper.INITIAL_SCALE_FACTOR = 10000000000;