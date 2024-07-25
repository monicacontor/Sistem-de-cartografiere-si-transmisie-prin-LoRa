#include <SPI.h>  // Librărie pentru comunicarea SPI
#include <LoRa.h> // Librărie pentru comunicarea LoRa

#define NSS 10   // Pinul de selectare a modulului LoRa
#define DIO0 2   // Pinul DIO0 al modulului LoRa

void setup() {
  Serial.begin(9600);  // Inițializează comunicarea serială la 9600 baud rate
  while (!Serial);  // Așteaptă deschiderea conexiunii seriale

  // Inițializare LoRa
  LoRa.setPins(NSS, -1, DIO0);  // Setează pinii pentru LoRa
  if (!LoRa.begin(868E6)) {  // Setează frecvența de 868 MHz
    Serial.println("Starting LoRa failed!");
    while (1);  // Blochează programul în cazul unei erori
  }
  Serial.println("LoRa inițializat!");
}

void loop() {
  // Verifică dacă există un pachet primit
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    // Pachet primit
    String distance = "";
    while (LoRa.available()) {
      distance += (char)LoRa.read();  // Citește datele primite
    }
    Serial.print("Distanța recepționată: ");
    Serial.println(distance);

   // Trimite datele la portul serial
    Serial.println(distance);
  }
}
