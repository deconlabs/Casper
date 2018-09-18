makeTextFile = function (text) {
    var data = new Blob([text], {type: 'text/plain'});

    // If we are replacing a previously generated file we need to
    // manually revoke the object URL to avoid memory leaks.
    if (textFile !== null) {
      window.URL.revokeObjectURL(textFile);
    }

    var textFile = window.URL.createObjectURL(data);

    // returns a URL you can use as a href
    return textFile;
};

doExperimentFigure3a = function() {
    var tau = 2000;
    var traceEpochStep = 100;
    var traceCounter = 0;
    var h = 0.25;
    
    var text = "j,tau,h,D_normal,D_noncensored,D_censored";
    // D: D=10000000, p/gamma: 1.0/21, 0.5/0.007, 0.3/0.00026, 0.2/0.00005, 0.1/0.000011, 0/0.0000022 
    var n = 2;
    var totalD = 100000;
    var baseDepositDependence = 0;
    var baseInterestFactor = 0.00017;
    var basePenaltyFactor = 0.0000002;

    var casperHonest = new Casper(totalD, h, baseInterestFactor, basePenaltyFactor, baseDepositDependence, 0);
    var casperAttack = new Casper(totalD, h, baseInterestFactor, basePenaltyFactor, baseDepositDependence, tau);
    var overtake = -1;
    var maxEpochs = 7002;
    
    for(var j=0;j<maxEpochs;j++)  {
        casperHonest.processEpoch();
        casperAttack.processEpoch();
        if(overtake == -1 && (casperHonest.getScaledDeposit(0) < casperAttack.getScaledDeposit(0))) {
            overtake = j;
            Dovertake = casperHonest.getScaledDeposit(0);
        }
        if(j > traceCounter*traceEpochStep) {
            traceCounter++;
            var atext = j+","+tau+","+h+","+casperHonest.getDepositChange(0)+","+casperAttack.getDepositChange(0)+","+casperAttack.getDepositChange(1);
            console.log(atext);
            text += "\n"+atext;
        }
    }
    
    var fileContents = document.getElementById('filecontents'); 
    fileContents.innerText = text; 
}

doExperimentFigure3b = function() {
    var tau = 2000;
    var traceEpochStep = 100;
    var traceCounter = 0;
    var h = 0.25;
    
    var text = "j,tau,h,D_normal,D_noncensored,D_censored";
    // D: D=10000000, p/gamma: 1.0/21, 0.5/0.007, 0.3/0.00026, 0.2/0.00005, 0.1/0.000011, 0/0.0000022 
    var n = 2;
    var totalD = 100000;
    var baseDepositDependence = 1;
    var baseInterestFactor = 20.;
    var basePenaltyFactor = 0.0000002;

    var casperHonest = new Casper(totalD, h, baseInterestFactor, basePenaltyFactor, baseDepositDependence, 0);
    var casperAttack = new Casper(totalD, h, baseInterestFactor, basePenaltyFactor, baseDepositDependence, tau);
    var overtake = -1;
    var maxEpochs = 7002;
    
    for(var j=0;j<maxEpochs;j++)  {
        casperHonest.processEpoch();
        casperAttack.processEpoch();
        if(overtake == -1 && (casperHonest.getScaledDeposit(0) < casperAttack.getScaledDeposit(0))) {
            overtake = j;
            Dovertake = casperHonest.getScaledDeposit(0);
        }
        if(j > traceCounter*traceEpochStep) {
            traceCounter++;
            var atext = j+","+tau+","+h+","+casperHonest.getDepositChange(0)+","+casperAttack.getDepositChange(0)+","+casperAttack.getDepositChange(1);
            console.log(atext);
            text += "\n"+atext;
        }
    }
    
    var fileContents = document.getElementById('filecontents'); 
    fileContents.innerText = text; 
}

doExperimentFigure4a = function() {
    var h = 0.00001;
    var startH = 0.3;
    var stepH = 0.001;
    var endH = 1.0;
    var baseMaxEpochs = 100000;
    
    var text = "h,first_finalization_epoch";

    for(var h=startH;h<endH;h+=stepH) {
        var n = 2;
        var eachValidatorD = 10000000;
        var baseInterestFactor = 0.007;
        var basePenaltyFactor = 0.0000002;
        var baseDepositDependence = 0.5;

        var casper = new Casper(eachValidatorD, h, baseInterestFactor, basePenaltyFactor, baseDepositDependence, maxEpochs, 0);
        var maxEpochs = baseMaxEpochs;
        for(var j=0;j<maxEpochs;j++)  {
            casper.processEpoch();
            if(casper.lastFinalizedEpoch > -1) {
                break;
            }
        }

        var atext = h+","+casper.getFinalizationEpoch();
        console.log(atext);
        text += "\n"+atext;
    }
    
    var fileContents = document.getElementById('filecontents'); 
    fileContents.innerText = text; 
}

doExperimentFigure4b = function() {
    var h = 0.00001;
    var startH = 0.3;
    var stepH = 0.001;
    var endH = 1.0;
    var baseMaxEpochs = 100000;
    
    var text = "h,first_finalization_epoch";

    for(var h=startH;h<endH;h+=stepH) {
        var n = 2;
        var eachValidatorD = 10000000;
        var baseInterestFactor = 0.007;
        var basePenaltyFactor = 0.0000002;
        var baseDepositDependence = 0.5;

        var casper = new Casper(eachValidatorD, h, baseInterestFactor, basePenaltyFactor, baseDepositDependence, maxEpochs, 1000);
        var maxEpochs = baseMaxEpochs;
        for(var j=0;j<maxEpochs;j++)  {
            casper.processEpoch();
            if(casper.lastFinalizedEpoch > -1) {
                break;
            }
        }

        var atext = h+","+casper.getFinalizationEpoch();
        console.log(atext);
        text += "\n"+atext;
    }
    
    var fileContents = document.getElementById('filecontents'); 
    fileContents.innerText = text; 
}