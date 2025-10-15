#include <SPI.h>
#include <MFRC522.h>

// Pinos do módulo RFID RC522
#define SS_PIN 10
#define RST_PIN 9

// LEDs e buzzer
#define LED_VERDE 5
#define LED_AMARELO 6
#define LED_VERMELHO 7
#define BUZZER 3

MFRC522 mfrc522(SS_PIN, RST_PIN);

// Lista de UIDs autorizados
const char* autorizados[] = {
  "BA2CFE03", // Cartão branco
  // "12345678", // Adicione outros UIDs aqui
};

String ultimoUID = "";
unsigned long ultimaLeitura = 0;
const unsigned long intervaloLeitura = 1000; // 1 segundo entre leituras

// Função de beep com frequência alta
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
  digitalWrite(LED_AMARELO, LOW);

  // Animação inicial
  Serial.println("INIT:Sistema iniciado");
  for (int i = 0; i < 2; i++) {
    digitalWrite(LED_AMARELO, HIGH);
    beep(1, 100, 100, 2500);
    delay(100);
    digitalWrite(LED_AMARELO, LOW);
    delay(100);
  }
  Serial.println("READY:Sistema pronto");
  digitalWrite(LED_AMARELO, HIGH);
}

void loop() {
  // Verifica se há um novo cartão
  if (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial()) {
    return;
  }

  // Evita leituras repetidas
  if (millis() - ultimaLeitura < intervaloLeitura) {
    return;
  }

  // Indica leitura
  digitalWrite(LED_AMARELO, LOW);
  beep(1, 150, 100, 2500);
  Serial.println("LENDO:Cartão detectado");

  // Captura o UID
  String uidString = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    if (mfrc522.uid.uidByte[i] < 0x10) uidString += "0";
    uidString += String(mfrc522.uid.uidByte[i], HEX);
  }
  uidString.toUpperCase();

  // Evita spam do mesmo UID
  if (uidString == ultimoUID && millis() - ultimaLeitura < 5000) {
    mfrc522.PICC_HaltA();
    return;
  }

  ultimoUID = uidString;
  ultimaLeitura = millis();

  // Verifica se está autorizado
  bool autorizado = false;
  for (unsigned int i = 0; i < sizeof(autorizados) / sizeof(autorizados[0]); i++) {
    if (uidString == autorizados[i]) {
      autorizado = true;
      break;
    }
  }

  if (autorizado) {
    Serial.println("AUTORIZADO:Acesso permitido");
    digitalWrite(LED_VERDE, HIGH);
    beep(3, 200, 150, 3000);
    delay(2000);
    digitalWrite(LED_VERDE, LOW);
  } else {
    Serial.println("NEGADO:Acesso negado");
    digitalWrite(LED_VERMELHO, HIGH);
    beep(2, 300, 150, 1800);
    delay(2000);
    digitalWrite(LED_VERMELHO, LOW);
  }

  Serial.println("READY:Sistema pronto");
  digitalWrite(LED_AMARELO, HIGH);
  mfrc522.PICC_HaltA();
}