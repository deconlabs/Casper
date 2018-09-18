class NodeDisplay {
    
    constructor(network) {
        this.network = network;
        this.node;
    }
    
    setNode(node) {
        this.node = node;
    }
    
    redraw() {
        var canvas = document.getElementById('nodeCanvas');
        var context = canvas.getContext('2d');
        context.clearRect(0, 0, canvas.width, canvas.height);
        if(this.node != null) {
            context.font = "16px Arial";
            context.fillText("node "+this.node.index,6,16);
            context.fillText("pos: ["+this.node.x+", "+this.node.y+"]",6,34);
            context.fillText("pp: "+this.node.pp,6,52);
            context.fillText("mem: "+this.node.mem,6,70);
            if(this.node.dns == "1") context.fillText("dns: yes",6,88);
            else context.fillText("dns: no",6,88);
            context.fillText("outgoing: "+this.node.outgoingConnections,6,106);
            context.fillText("bc length: "+this.node.blockchain.length,6,124);
            context.fillText("#mined: "+this.node.getNumBlocksMined()+"/"+this.node.blockchain.length,6,142);
            context.fillText("#orphans: "+this.node.orphans.length,6,160);
        }
    }
}