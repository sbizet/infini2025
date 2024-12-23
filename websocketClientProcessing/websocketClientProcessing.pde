import websockets.*;
WebsocketClient wsc;
SimulChariot simul;
String txtAff = "";

void setup() {
  size(400, 200);
  fill(255);
  textSize(24);
  wsc= new WebsocketClient(this, "ws://localhost:8484");
  simul = new SimulChariot();
  int[] tabRecu = {65,1,100,20,20,0,0,0};
  simul.maj(tabRecu);
}

void draw() {
  background(0);
  
  text(txtAff,10,50);
}

void webSocketEvent(String msg) {
  int[] tabRecu = trameToIntTab(msg);
  printTab(tabRecu);
  
  simul.maj(tabRecu);
  
  int[] tabEnvoi = simul.getTrameEnvoi();
  wsc.sendMessage(trameToString(tabEnvoi));
}

String trameToString(int[] tab) {
  String s = "";
  for (int i = 0; i<tab.length; i++) {
    s+=hex(tab[i],2);
  }
  return s;
}

int[] trameToIntTab(String s) {
  int[] retour = new int[s.length()/2];
  for (int i=0; i<retour.length; i++) {
    retour[i] = unhex(s.substring(i*2,i*2+2));
  }
  return retour;
}


void printTab(int[] _tab) {
  if(_tab[0] == 65) txtAff = "Client reçoit : \n";
  for (int i=0; i<_tab.length; i++) {
    txtAff+=_tab[i]+";";
  }
  txtAff+="\n";
}
