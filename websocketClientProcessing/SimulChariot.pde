/*
Trame Recue
Octet n° 0 : 65 ou 66 ('A' ou 'B' en ASCII) : information sur le chariot concerné A ou B
Octet n°1 : 0 ou 1 : le chariot est mis en marche ou arrêté.
Octet n°2 : 0 à 255 : Vmot = information pour le réglage de la vitesse du moteur
Octet n°3 : 0 à 180 : Pan
Octet n°4 : 0 à 180 : Tilt
Octet n°5 : 0 octet bidon
Octet n°6 : 0 octet bidon
Octet n°7 : 0 octet bidon

Trame envoyée :
Octet n°0 : 65 ou 66 ('A' ou 'B' en ASCII) : information sur le chariot A ou B envoyant l'information
Octet n°1 : Vbat (0 à 255) : Une information sur la tension au niveau de la batterie (255 correspondant à 15V par exemple) 
Octet n°2 : inclinaison  (0 à 255) information issue de l'accélérometre + gyroscope
Octet n°3 : wr (0 à 255) information issue de l'accélérometre + gyroscope
Octet n°4 : vR (0 à 255) : vitesse réelle
Octet n°5 : 0 octet bidon
Octet n°6 : 0 octet bidon
Octet n°7 : 0 octet bidon
 */
 
public class SimulChariot {
  int vRotMax = 120;
  float perimetreRoue = PI*0.1;
  float vMax = (perimetreRoue*vRotMax)/60;
  float T = 200;

  int lTrameRecu = 8;
  int lTrameEnvoi = 8;

  int[] trameRecu = new int [lTrameRecu];
  int[] trameEnvoi  = {'A', 200, 150, 100, 0, 0, 0, 0};

  float angle = 0;
  float wr = 0;
  float dA = 0;
  float dB = 0;
  long tA = 0;
  long tB = 5000;

  long tempTA = 0;
  long tempTB = 0;

  float vRA = 0;
  float vRB = 0;

  SimulChariot() {
  }
  
  void maj(int[] _trameRecu){
    trameRecu = _trameRecu;
    if (trameRecu[0] == 'A'){
      float vA = 0;
      if(trameRecu[1] != 0){
        vA = trameRecu[2]*vMax/255;
      }
      if(millis()-tempTA >= 100){
        vRA = calcVr(vA, millis()-tempTA, vRA);
        tempTA = millis();
      }             
      trameEnvoi[4] = int((vRA*255.0)/vMax);
      dA = simulData(vRA, dA, millis()-tA);
      tA = millis();
      trameEnvoi[0] = 65;
    }
    if (trameRecu[0] == 'B'){
      float vB = 0;
      if(trameRecu[1] != 0){
        vB = trameRecu[2]*vMax/255;
      }
      if(millis()-tempTB >= 100){
        vRB = calcVr(vB, millis()-tempTB, vRB);
        tempTB = millis();
      }             
      trameEnvoi[4] = int((vRB*255.0)/vMax);
      dB = simulData(vRB, dB, millis()-tB);
      tB = millis();
      trameEnvoi[0] = 66;
    }
    if (trameRecu[0] == 'A' || (trameRecu[0] == 'B' && millis() > 500)){
      
      trameEnvoi[2] = int((angle+PI)*255/(2*PI));
      trameEnvoi[3] = int((wr/1.5+2.5)*255/(2*2.5));
      trameEnvoi[1] = int(180 + random(10));
      trameEnvoi[5] = 0;
      trameEnvoi[6] = 0;
      trameEnvoi[7] = 0;
      
    }
  }
  
  int[] getTrameEnvoi(){
    return trameEnvoi;
  }

  float simulData(float V, float d, long t) {
    float R = 0.61;
    float l = 1.5;
    float alpha = atan(2*R/l);
    d += (t/1000.0)*V;
    if (d <= (l/2)) {
      wr = 0;
      angle = PI/2 + alpha;
    } else if (d <= (l/2+(PI+2*alpha)*R)) {
      wr = -V/R;
      angle = (PI/2 + alpha) - ((d-(l/2))/((PI+2*alpha)*R) * (PI+2*alpha));
    } else if (d <= (3*l/2+(PI+2*alpha)*R)) {
      wr = 0;
      angle = -PI/2 - alpha;
    } else if (d <= (3*l/2+(2*PI+4*alpha)*R)) {
      wr = V/R;
      angle = (-PI/2 - alpha) + ((d-(3*l/2+(PI+2*alpha)*R))/((PI+2*alpha)*R) * (PI+2*alpha));
    } else {
      wr = 0;
      angle = PI/2 + alpha;
    }
    if (d >= (2*l + (2*PI + 4*alpha) * R)) {
      d = 0;
    }
    return d;
  }

  float calcVr(float v, long t, float vR) {
    float newVR = (v+((0.5*vR)/(t/1000.0)))/((0.5/(t/1000.0))+1);
    
    return newVR;
  }
}
