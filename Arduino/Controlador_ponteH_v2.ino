 // Pinos do motor 1
 // Pinos: 10 direito - 11 esquerda
 #define motor1D  10
 #define motor1E  11

 // Pinos do motor 2
 // Pinos: 9 direito - 3 esquerda
 #define motor2D  9
 #define motor2E  3
 
 //Não foi utilizado as portas PWM 5 e 6 para evitar 
 // diferença de rotação do motor pois as mesmas utilização
 // 1KHz ao contrario da portas 3,9,10,11 que utilizam 500Hz

String inputString;
boolean stringComplete = false;

String vel_serial;

int vel_final = 0;
int vel_atual = 0;

int comando = 0;
int trocou_comando = 0;

// ============================================================================================================================================================
// --------------------------------------------------------------------------- SETUP --------------------------------------------------------------------------
// ============================================================================================================================================================
void setup() {
  
  //Configuração dos pinos
  pinMode(motor1D,OUTPUT);
  pinMode(motor1E,OUTPUT);
  pinMode(motor2D,OUTPUT);
  pinMode(motor2E,OUTPUT);
  
  //Inicialização da portas
  analogWrite(motor1D,0);
  analogWrite(motor1E,0);
  analogWrite(motor2D,0);
  analogWrite(motor2E,0);
    
  pinMode(13, OUTPUT); 
   
  Serial.begin(9600);	// Debugging only 
  digitalWrite(13, LOW); 
  
  // MSG inicial da comunicação serial
  Serial.println("*********************************************************");
  Serial.println("*    E.N.E. - v 1.0 - Comunicação com os motores      *");
  Serial.println("*********************************************************");
  Serial.println(" "); 
  
}
// ============================================================================================================================================================
// --------------------------------------------------------------------------- SETUP --------------------------------------------------------------------------
// ============================================================================================================================================================

// ************************************************************************************************************************************************************

// ============================================================================================================================================================
// --------------------------------------------------------------------------- LOOP ---------------------------------------------------------------------------
// ============================================================================================================================================================
void loop() {
    
    trocou_comando = comando;  
// --- Comunicação Serial ---
   if(stringComplete){
     
       vel_serial = inputString.substring(1);
       
       Serial.print("Comando recebido com sucesso! (");
       Serial.print(inputString.charAt(0));       
       Serial.print(") - (");
       Serial.print(vel_serial.toInt());
       Serial.println(")");

       vel_final = vel_serial.toInt();
       comando = inputString.charAt(0) - 48;
       
       //comandos(chtemp,ang.toInt());     
     
       stringComplete = false;
       inputString = "";
   }
//------------------

  if(trocou_comando != comando){
    vel_atual -= (vel_atual/2);

    if(vel_atual < 0)
      vel_atual = 0;
  }

//--------- Incremento/Redução da velocidade
   if(vel_atual != vel_final){

      if(vel_atual < vel_final){

          if(vel_atual < 240){
            vel_atual += 10;
          }

      }

      if(vel_atual > vel_final){

        if(vel_atual >= 10){
          vel_atual -= 10;
        }
            
      }     
      
   }
//--------------------------------------

//------ Comando dos motores
  if(comando == 1){ //comando = 1 -> os dois motores para frente
      Serial.println("Motores para frente!");
      analogWrite(motor1E, 0);
      analogWrite(motor2E, 0);
      analogWrite(motor1D, vel_atual);        
      analogWrite(motor2D, vel_atual);
  }else if(comando == 2){ //comando = 2 -> os dois motores para traz
      Serial.println("Motores para traz!");
      analogWrite(motor1D, 0);
      analogWrite(motor2D, 0);
      analogWrite(motor1E, vel_atual);        
      analogWrite(motor2E, vel_atual);
  }else if(comando == 3){ //comando = 3 -> para direita
      Serial.println("Gira para direita!");
      analogWrite(motor1E, 0);
      analogWrite(motor2D, 0);
      analogWrite(motor1D, vel_atual);        
      analogWrite(motor2E, vel_atual);
  }else if(comando == 4){ //comando = 4 -> para direita
      Serial.println("Gira para esquerda!");
      analogWrite(motor1D, 0);
      analogWrite(motor2E, 0);
      analogWrite(motor1E, vel_atual);  
      analogWrite(motor2D, vel_atual); 
  }else{ // parada de emergencia
      Serial.println("Parar!");
      analogWrite(motor1D,0);
      analogWrite(motor1E,0);
      analogWrite(motor2D,0);
      analogWrite(motor2E,0); 
  }
 
  delay(100);
}
// ============================================================================================================================================================
// --------------------------------------------------------------------------- LOOP ---------------------------------------------------------------------------
// ============================================================================================================================================================

//------------------------------------------ SERIAL -------------------------------------------------------
void serialEvent(){
  while(Serial.available()){
     char inChar = (char)Serial.read();
     inputString += inChar;
     
     if(inChar == '\n'){
        stringComplete = true; 
     }
  }  
}

