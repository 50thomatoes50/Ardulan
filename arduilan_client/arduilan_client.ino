#include <SPI.h>        
#include <Ethernet.h>
#include <EthernetUdp.h>
IPAddress server;
byte entre[6],i,stats[9],sorti[6];
unsigned long time=65535, time1;
#define timeout 6000
  // An EthernetUDP instance to let us send and receive packets over UDP
EthernetUDP Udp;

boolean servernotfound = true, stat=false;
char packetBuffer[UDP_TX_PACKET_MAX_SIZE],temp[20],stcompare[3]="st";
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
#define ID "0"

void setup(){
  Serial.begin(9600);
  
  pinMode(10, OUTPUT); //Device select W5100 (ethernet)
  pinMode(4, OUTPUT); //Device select SD
  digitalWrite(4,HIGH);//Desactivation SD
  #if defined(__AVR_ATmega2560__)
    pinMode(53, OUTPUT);
    //the hardware SS pin, 53,must be kept as an output or the SPI interface won't work. 
  #endif
  Serial.print("Arduino ");
  #if defined(__AVR_ATmega2560__)
    Serial.println("MEGA");
    for(int i = 0; i< 50; i++){
      if(i != 4 or i!=10 or i!=11 or i!=12 or i!=13)
        pinMode(i, INPUT); 
    }
    /*pinMode(22, INPUT); 
    pinMode(23, INPUT); 
    pinMode(24, INPUT); 
    pinMode(25, INPUT); 
    pinMode(26, INPUT); 
    pinMode(27, INPUT); 
    pinMode(28, INPUT); 
    pinMode(29, INPUT); */
  #endif
  #if defined(__AVR_ATmega32U4__)
    Serial.println("Leonardo");
  #endif
  
  if (Ethernet.begin(mac) == 0) 
  {
    while(1)
    {
      Serial.println("Failed to configure Ethernet using DHCP");
      delay(2000);
    }
  }
  else
  {
    Serial.println(Ethernet.localIP());
  }
   Udp.begin(5050); 
  findserver();
}
  
void loop(){  
  int packetSize = Udp.parsePacket();
  if(packetSize)
  {
    time = millis();
    erasebuffer();
    Udp.read(packetBuffer,UDP_TX_PACKET_MAX_SIZE);

    if( strcmp(packetBuffer,"Ardulan1") == 0){
      return;}
      
    //Serial.println(packetBuffer);      
    if( strcmp(packetBuffer,"qr") == 0){
      Serial.print("Server disconnected");
      servernotfound=1;
      findserver();
      return;
    }
    
    if(  memcmp ( packetBuffer , stcompare, 2 ) == 0)   ////ST
      {
       //Serial.print(packetBuffer);
       pinstatarray(packetBuffer[2] , 2);
       pinstatarray(packetBuffer[3] , 6);
       pinstatarray(packetBuffer[4] , 22);
       pinstatarray(packetBuffer[5] , 26);
       pinstatarray(packetBuffer[6] , 30);
       pinstatarray(packetBuffer[7] , 34);
       pinstatarray(packetBuffer[8] , 38);
       pinstatarray(packetBuffer[9] , 42);
       pinstatarray(packetBuffer[10] , 46);
       for(byte z = 2; z<11 ; z++)
       {
         stats[z-2] = packetBuffer[z];
       }
       for(byte z = 0; z<6 ; z++)
       {
         sorti[z] = packetBuffer[z+10];
       }
      }
      
    if( strcmp(packetBuffer,"in") == 0)
      {
      entre[0]=pinio(7)*32+pinio(6)*16+pinio(5)*8+pinio(3)*2+pinio(2);
      entre[1]=digitalRead(9)*2+digitalRead(8);
      entre[2]=digitalRead(29)*128+digitalRead(28)*64+digitalRead(27)*32+digitalRead(26)*16+digitalRead(25)*8+digitalRead(24)*4+digitalRead(23)*2+digitalRead(22);
      entre[3]=digitalRead(37)*128+digitalRead(36)*64+digitalRead(35)*32+digitalRead(34)*16+digitalRead(33)*8+digitalRead(32)*4+digitalRead(31)*2+digitalRead(30);
      entre[4]=digitalRead(45)*128+digitalRead(44)*64+digitalRead(43)*32+digitalRead(42)*16+digitalRead(41)*8+digitalRead(40)*4+digitalRead(39)*2+digitalRead(38);
      entre[5]=digitalRead(49)*8+digitalRead(48)*4+digitalRead(47)*2+digitalRead(46);
      Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
      i=0;temp[1]=0;temp[2]=0;temp[3]=0;temp[4]=0;temp[5]=0;
      Udp.write(entre[0]);
      Udp.write(entre[1]);
      Udp.write(entre[2]);
      Udp.write(entre[3]);
      Udp.write(entre[4]);
      Udp.write(entre[5]);
      Udp.endPacket();
    }

    if( strcmp(packetBuffer,"Actu") == 0)
      {
      Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
      Udp.write("ACK");
      Udp.endPacket();
      }

  }
  if(millis()<timeout)
    time1=0;
  else
  {
    time1 = millis();
    time1 -= timeout;
  }
  if( time1 > time){
      Serial.println("Server timeout");
      Serial.print("time=");
      Serial.print(time);
      Serial.print("\ttime=");
      Serial.println(time1);
      servernotfound=1;
      findserver();
   }
    
}
boolean pinio( byte nb)
{
  int j=nb,k,statarr=0;
  while(j>4)
  {
    j-=4;
    statarr++;  
  }
  switch(j){
    case 1:
      k = stats[statarr]>>2;
    break;
    case 2:
      k = stats[statarr]>>4;
    break;
    case 3:
      k = stats[statarr]>>6;
    break;
  }
  k=k&3;
  switch(k){
    case 0:
      pinMode(nb, OUTPUT);
      return 0;
    break;
    case 1:
      pinMode(nb, INPUT);
      return digitalRead(nb);
    break;
  }
  
    

}
  

void pinstatarray(byte data,byte start)
{
    pinstat( start, stat&3 );
    pinstat( start+1, stat>>2&3 );
    pinstat( start+2, stat>>4&3 );
    pinstat( start+3, stat>>6&3 );
}
void pinstat(byte pin, byte stat)
{
  if(pin == 4)
    return;
  switch(stat)
  {
    case 0: 
     pinMode(pin, OUTPUT); 
    break;
    case 1: 
     pinMode(pin, OUTPUT); 
    break;
    case 2: 
     pinMode(pin, OUTPUT); 
    break;
    case 3: 
     pinMode(pin, OUTPUT); 
    break;
  }
  
}
  
void findserver(){
  Serial.println("finding server..");
  while(servernotfound){
    int packetSize = Udp.parsePacket();
    if(packetSize)
    {
      //Serial.print("Received packet of size ");
      //Serial.print(packetSize);
      //Serial.print("From ");
      /*for (int i =0; i < 4; i++)
      {
        Serial.print(remote[i], DEC);
        if (i < 3)
        {
          Serial.print(".");
        }
      }
      Serial.print(", port ");
      Serial.print(Udp.remotePort());*/
  
      // read the packet into packetBufffer
      Udp.read(packetBuffer,UDP_TX_PACKET_MAX_SIZE);
      //Serial.print("Contents:");
      //Serial.println(packetBuffer);
      /*for(int i =0;packetBuffer[i]!=0;i++){
        Serial.print(packetBuffer[i],HEX);
        }
      Serial.print("\n");*/
      
      if( strcmp(packetBuffer,"Ardulan1") == 0)
      {
        server = Udp.remoteIP();
        servernotfound = false;
        Serial.print("Server found:");
        for (int i =0; i < 4; i++)
        {
          Serial.print(server[i], DEC);
          if (i < 3)
          {
            Serial.print(".");
          }
        }
        Serial.print("\n");
        Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
        #if defined(__AVR_ATmega2560__)
          Udp.write("MEGA");
        #endif
        #if defined(__AVR_ATmega32U4__)
          Udp.write("Leo");
        #endif
        Udp.write("!");
        Udp.write(ID);
        Udp.endPacket();
        time = millis();
        Serial.print("time=");
        Serial.println(time);
      }
      
      erasebuffer();

    }
  }
}
void erasebuffer(){
 for(int i=0; i<UDP_TX_PACKET_MAX_SIZE; i++)//Vider le buffer
 packetBuffer[i]=0;
      }
