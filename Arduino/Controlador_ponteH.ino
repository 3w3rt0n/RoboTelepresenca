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
 
 //Pinos de entrada
 #define v12 0         //Medição da bateria de 12 volts (Motores)
 #define v5 1          //Medição da bateria de 5 volts (Arduino e Raspberry) 
 #define temp1 2       //Temperatura dos moftes do motor 1 
 #define temp2 3       //Temperatura dos moftes do motor 2 
 
 
int temp = 0;


//Sensores analogicos
float sv5 = 0;
float sv12 = 0;
float t1 = 0;
float t2 = 0;

String inputString;
boolean stringComplete = false;

int parar = 0;
int motor = 0;
int angulo = 0;
String ang;

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
    
      
// --- Comunicação Serial ---
   if(stringComplete){
     
       ang = inputString.substring(1);
       
       Serial.print("Comando recebido com sucesso! (");
       Serial.print(inputString.charAt(0));       
       Serial.print(") - (");
       Serial.print(ang.toInt());
       Serial.println(")");
       
       int chtemp = inputString.charAt(0) - 48;
       
       comandos(chtemp,ang.toInt());     
     
       stringComplete = false;
       inputString = "";
   }
// --- Comunicação Serial ---

   if(!parar){
      analogWrite(motor1D,0);
      analogWrite(motor1E,0);
      analogWrite(motor2D,0);
      analogWrite(motor2E,0); 
   }else{
     parar--;
   } 

   
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

void comandos(int motor, int vel){
  /*
    Formato do comando XYYY
    X- motor (1 ou 2)
    YYY- velocidade
    001-499 - frente
    501-999 - traz
  */
  if(motor == 1){ 
    // 1000 - motor parado
    // 1001 - 1255 - motor para frente
    // 1501 - 1755 - motor para tras   
    if(vel == 0){
      analogWrite(motor1D,0);
      analogWrite(motor1E,0);
    }else if(vel > 0 && vel < 256){
       analogWrite(motor1E, 0);
       analogWrite(motor1D, vel); 
    }else if(vel > 500 && vel < 756){
       analogWrite(motor1D, 0);
       analogWrite(motor1E, (vel-500)); 
    }else
      Serial.println(" Comando invalido - velocidade nao especificado ou especificada foram do parametros!");
  }else if(motor == 2){
    // 2000 - motor parado
    // 2001 - 2255 - motor para frente
    // 2501 - 2755 - motor para tras 
    if(vel == 0){
      analogWrite(motor2D,0);
      analogWrite(motor2E,0);
    }else if(vel > 0 && vel < 256){
       analogWrite(motor2E, 0);
       analogWrite(motor2D, vel); 
    }else if(vel > 500 && vel < 756){
       analogWrite(motor2D, 0);
       analogWrite(motor2E, (vel-500)); 
    }else
      Serial.println(" Comando invalido - velocidade nao especificado ou especificada foram do parametros!");
  }else if(motor == 3){
    // acionar os dois motores para frente ou para traz
    // 3000 - motores parados
    // 3001 - 3255 - motores para frente
    // 3501 - 3755 - motores para tras 
    if(vel == 0){
      analogWrite(motor1D,0);
      analogWrite(motor1E,0);
      analogWrite(motor2D,0);
      analogWrite(motor2E,0);      
    }else if(vel > 0 && vel < 256){
       analogWrite(motor1E, 0);
       analogWrite(motor2E, 0);
       analogWrite(motor1D, vel);        
       analogWrite(motor2D, vel); 
    }else if(vel > 500 && vel < 756){
       analogWrite(motor1D, 0);
       analogWrite(motor2D, 0);
       analogWrite(motor1E, (vel-500));  
       analogWrite(motor2E, (vel-500));  
    }else
      Serial.println(" Comando invalido - velocidade nao especificado ou especificada foram do parametros!");
  }else if(motor == 4){
    // gira para direita ou esquerda
    // 4000 - motor parado
    // 4001 - 4255 - gira para direita por 10 segundos
    // 4501 - 4755 - gira para esquerda por 10 segundos
    if(vel == 0){
      analogWrite(motor1D,0);
      analogWrite(motor1E,0);
      analogWrite(motor2D,0);
      analogWrite(motor2E,0);      
    }else if(vel > 0 && vel < 256){
       analogWrite(motor1E, 0);
       analogWrite(motor2D, 0);
       analogWrite(motor1D, vel);        
       analogWrite(motor2E, vel); 
    }else if(vel > 500 && vel < 756){
       analogWrite(motor1D, 0);
       analogWrite(motor2E, 0);
       analogWrite(motor1E, (vel-500));  
       analogWrite(motor2D, (vel-500));  
    }else
      Serial.println(" Comando invalido - velocidade nao especificado ou especificada foram do parametros!"); 
      
    //gira durante 500ms  
    delay(1000);
    analogWrite(motor1D,0);
    analogWrite(motor1E,0);
    analogWrite(motor2D,0);
    analogWrite(motor2E,0); 
  
  }else if(motor == 5){ 
    // 5000 - motor parado
    // 5001 - 5255 - motor para frente
    // 5501 - 5755 - motor para tras   
    if(vel == 0){
      analogWrite(motor1D,0);
      analogWrite(motor1E,0);
    }else if(vel > 0 && vel < 256){
       analogWrite(motor1E, 0);
       analogWrite(motor1D, vel); 
       parar = 10;
    }else if(vel > 500 && vel < 756){
       analogWrite(motor1D, 0);
       analogWrite(motor1E, (vel-500)); 
       parar = 10;
    }else
      Serial.println(" Comando invalido - velocidade nao especificado ou especificada foram do parametros!");
      
  }else if(motor == 6){ 
    // 6000 - motor parado
    // 6001 - 6255 - motor para frente
    // 6501 - 6755 - motor para tras   
    if(vel == 0){
      analogWrite(motor2D,0);
      analogWrite(motor2E,0);
    }else if(vel > 0 && vel < 256){
       analogWrite(motor2E, 0);
       analogWrite(motor2D, vel); 
       parar = 10;
    }else if(vel > 500 && vel < 756){
       analogWrite(motor2D, 0);
       analogWrite(motor2E, (vel-500)); 
       parar = 10;
    }else
      Serial.println(" Comando invalido - velocidade nao especificado ou especificada foram do parametros!");
      
   }else if(motor == 7){
    // acionar os dois motores para frente ou para traz
    // 7000 - motores parados
    // 7001 - 7255 - motores para frente
    // 7501 - 7755 - motores para tras 
    if(vel == 0){
      analogWrite(motor1D,0);
      analogWrite(motor1E,0);
      analogWrite(motor2D,0);
      analogWrite(motor2E,0);      
    }else if(vel > 0 && vel < 256){
       analogWrite(motor1E, 0);
       analogWrite(motor2E, 0);
       analogWrite(motor1D, vel);        
       analogWrite(motor2D, vel); 
       parar = 10;
    }else if(vel > 500 && vel < 756){
       analogWrite(motor1D, 0);
       analogWrite(motor2D, 0);
       analogWrite(motor1E, (vel-500));  
       analogWrite(motor2E, (vel-500));  
       parar = 10;
    }else
      Serial.println(" Comando invalido - velocidade nao especificado ou especificada foram do parametros!");
     
  }else if(motor == 9){
    //leitura das portas analogicas
    // 9100 - 9199 - retorna voltagem da bateria do motores
    // 9200 - 9299 - retorna voltagem da bateria do arduino\raspberry
    // 9300 - 9399 - retorna temperatura dos mosfet do motor 1
    // 9400 - 9499 - retorna temperatura dos mosfet do motor 2
    if(vel > 0 && vel < 200){
       Serial.print(" Voltagem da bateria dos motores: ");
       sv12 = 5.0 * analogRead(v12) / 1024.0;
       Serial.print(map(sv12, 0.0, 5.0, 0.0, 12.0)); //valor errado precisa ser corrigido
       Serial.println(" v");
    }else if(vel > 199 && vel < 300){
       Serial.print(" Voltagem da bateria do Arduino\\Raspberry: ");
       sv5 = 5.0 * analogRead(v5) / 1024.0;
       Serial.print(sv5*2);
       Serial.println(" v"); 
    }else if(vel > 299 && vel < 400){
       Serial.print(" Temperatura dos mosfets do motor 1: ");       
       t1 = 5.0 * analogRead(temp1) / 1024.0;     
       Serial.print((1.8663 - t1) / 0.01169 );
       Serial.println(" C");
    }else if(vel > 399 && vel < 500){
       Serial.print(" Temperatura dos mosfets do motor 2: ");
       t2 = 5.0 * analogRead(temp2) / 1024.0;           
       Serial.print((1.8663 - t2) / 0.01169 );
       Serial.println(" C");  
    }else
       Serial.println(" Comando invalido - velocidade nao especificado ou especificada foram do parametros!"); 
  
  }else 
    Serial.println(" Comando invalido - motor nao especificado!");
  
  
}
