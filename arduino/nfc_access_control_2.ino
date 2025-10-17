#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9
#define LED_VERDE 5
#define LED_AMARELO 6
#define LED_VERMELHO 7
#define BUZZER 3

MFRC522 mfrc522(SS_PIN, RST_PIN);

String ultimoUID = "";
unsigned long ultimaLeitura = 0;
const unsigned long intervaloLeitura = 1000;

void beep(int vezes, int duracao = 150, int pausa = 100, int frequencia = 2000) {
  for (int i = 0; i < vezes; i++) {
    tone(BUZZER, frequencia);
    delay(duracao);
    noTone(BUZZER);
    delay(pausa);
  }
}

void setup() {
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();

  pinMode(LED_VERDE, OUTPUT);
  pinMode(LED_AMARELO, OUTPUT);
  pinMode(LED_VERMELHO, OUTPUT);
  pinMode(BUZZER, OUTPUT);

  digitalWrite(LED_VERDE, LOW);
  digitalWrite(LED_VERMELHO, LOW);
  digitalWrite(LED_AMARELO, HIGH);

  Serial.println("READY:Sistema pronto");
}

void loop() {
  if (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial())
    return;

  if (millis() - ultimaLeitura < intervaloLeitura)
    return;

  digitalWrite(LED_AMARELO, LOW);
  beep(1, 150, 100, 2500);
  Serial.println("LENDO:Cartão detectado");

  String uidString = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    if (mfrc522.uid.uidByte[i] < 0x10) uidString += "0";
    uidString += String(mfrc522.uid.uidByte[i], HEX);
  }
  uidString.toUpperCase();

  if (uidString == ultimoUID && millis() - ultimaLeitura < 5000)
    return;

  ultimoUID = uidString;
  ultimaLeitura = millis();

  Serial.print("UID:");
  Serial.println(uidString);

  // Aguarda resposta do Python
  unsigned long inicio = millis();
  while (millis() - inicio < 3000) {
    if (Serial.available()) {
      char resposta = Serial.read();
      if (resposta == 'A') {
        Serial.println("AUTORIZADO:Acesso permitido");
        digitalWrite(LED_VERDE, HIGH);
        beep(3, 200, 150, 3000);
        delay(2000);
        digitalWrite(LED_VERDE, LOW);
      } else if (resposta == 'N') {
        Serial.println("NEGADO:Acesso negado");
        digitalWrite(LED_VERMELHO, HIGH);
        beep(2, 300, 150, 1800);
        delay(2000);
        digitalWrite(LED_VERMELHO, LOW);
      }
      break;
    }
  }

  Serial.println("READY:Sistema pronto");
  digitalWrite(LED_AMARELO, HIGH);
  mfrc522.PICC_HaltA();
}
