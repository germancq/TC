#include <Arduino.h>
#include <ArduinoJson.h>
#include <header.h>

#define pin_descarga 11
#define pin_carga 13
#define pin_Condensador A0

#define DESCARGA 1
#define CARGA 0

StaticJsonDocument<256> doc;

String str = "";
float initial_time = 0.0;

void setup() {
  pinMode(pin_carga, OUTPUT);
  pinMode(pin_descarga, OUTPUT);
  pinMode(5,OUTPUT);
  conf_descarga();
  Serial.begin(115200);
}

// the loop function runs over and over again forever
void loop() {
  if(Serial.available() > 0){
    read_from_python();
  }
}

void read_from_python(){
   str = Serial.readString();
   if(str == "carga"){
        digitalWrite(5,HIGH);

    conf_carga();
   }
   else if(str == "descarga"){  
    conf_descarga();
   }
   else if(str == "read"){
    lectura_condensador(initial_time);
   }
   

}

void conf_descarga(){
  // en la configuracion del circuito los pines conduciran a GND
   // produciendo cortocircuito.
   pinMode(pin_descarga,OUTPUT);
   pinMode(pin_carga,OUTPUT);
   digitalWrite(pin_carga,LOW);
   digitalWrite(pin_descarga,LOW);
   //initial_time = millis();
}

void conf_carga(){
  // en la configuracion del circ. hay que producir un circ. abierto
  // en la parte de descarga es decir I = 0. 
  // esto lo conseguiremos con Alta Impedancia en el pin de descarga
  pinMode(pin_descarga,INPUT);
  pinMode(pin_carga,OUTPUT);
  digitalWrite(pin_carga,HIGH);
  //initial_time = millis();
}


float lectura_condensador(float initial_time){
  int lectura_analogica = analogRead(pin_Condensador);
  float current_time = millis() - initial_time;
  float vc = (lectura_analogica / 1023.0) * 5.0;
  //envio del valor por puerto serie
  doc["vc"] = vc;
  doc["time"] = current_time/1000.0;
  serializeJson(doc,Serial);
  
  Serial.print('\n');
  Serial.flush();
  return vc;
}