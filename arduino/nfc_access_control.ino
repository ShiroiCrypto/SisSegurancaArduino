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
String autorizados[] = {
  "BA2CFE03"   // ✅ Cartão branco autorizado
};

// --- Função de beep com frequência alta ---
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

  // Animação inicial no console
  Serial.println("🔒 Sistema de Controle de Acesso NFC 🚀");
  Serial.println("=================================");
  for (int i = 0; i < 2; i++) {
    digitalWrite(LED_AMARELO, HIGH);
    beep(1, 100, 100, 2500);
    Serial.println("🟡 Inicializando...");
    delay(100);
    digitalWrite(LED_AMARELO, LOW);
    delay(100);
  }
  Serial.println("✅ Sistema pronto! Aproxime o cartão... 😎");
  Serial.println("=================================");
  Serial.println("INIT:Sistema iniciado");
  digitalWrite(LED_AMARELO, HIGH);
}

void loop() {
  if (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial()) {
    return;
  }

  // Indica leitura
  digitalWrite(LED_AMARELO, LOW);
  beep(1, 150, 100, 2500);
  Serial.println("=================================");
  Serial.println("📶 Cartão detectado! Lendo... 🔍");
  Serial.println("LENDO:Cartão detectado");

  // Captura o UID
  String uidString = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    if (mfrc522.uid.uidByte[i] < 0x10) uidString += "0";
    uidString += String(mfrc522.uid.uidByte[i], HEX);
  }
  uidString.toUpperCase();

  Serial.print("🔑 UID: ");
  Serial.println(uidString);
  Serial.print("UID:");
  Serial.println(uidString);

  // Verifica se está autorizado
  bool autorizado = false;
  for (String id : autorizados) {
    if (uidString == id) {
      autorizado = true;
      break;
    }
  }

  if (autorizado) {
    Serial.println("✅ Acesso AUTORIZADO! 🎉");
    Serial.println("AUTORIZADO:Acesso permitido");
    digitalWrite(LED_VERDE, HIGH);
    beep(3, 200, 150, 3000);  // 3 bipes altos
    delay(2000);
    digitalWrite(LED_VERDE, LOW);
  } else {
    Serial.println("❌ Acesso NEGADO! 🚨");
    Serial.println("NEGADO:Acesso negado");
    digitalWrite(LED_VERMELHO, HIGH);
    beep(2, 300, 150, 1800);  // 2 bipes graves
    delay(2000);
    digitalWrite(LED_VERMELHO, LOW);
  }

  Serial.println("🟡 Sistema pronto para nova leitura... 😎");
  Serial.println("READY:Sistema pronto");
  Serial.println("=================================");
  digitalWrite(LED_AMARELO, HIGH);
  mfrc522.PICC_HaltA(); // Para a leitura do cartão atual
  delay(500); // Evita leituras duplicadas
}