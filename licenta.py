import serial  # Librărie pentru comunicarea serială
import requests  # Librărie pentru cereri HTTP

# Configurația InfluxDB
influxdb_server = "http://192.168.100.11:8086"  # URL-ul serverului InfluxDB
influxdb_token = "byZ34CoLu3uO4y8KvOK_0D394sBSC2GRYXD4x3-EkUQnAoc6tsMjXDavoyxh3ZGI9uAEME4WaUg61LCenCZcCQ=="  # Tokenul de autorizare pentru InfluxDB
influxdb_org = "proiect_licenta"  # Numele organizației din InfluxDB
influxdb_bucket = "date_senzor"  # Numele bucket-ului din InfluxDB

# Configurația portului serial
serial_port = 'COM7'  # Portul serial la care este conectat Arduino
baud_rate = 9600  # Baud rate-ul pentru comunicația serială

# Initializează conexiunea serială
ser = serial.Serial(serial_port, baud_rate)

def send_to_influxdb(value):
    #Funcție pentru trimiterea datelor către InfluxDB
    url = f"{influxdb_server}/api/v2/write?org={influxdb_org}&bucket={influxdb_bucket}&precision=s"
    headers = {
        "Authorization": f"Token {influxdb_token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = f"ultrasonic_sensor,location=lab value={value}"
    response = requests.post(url, headers=headers, data=data)  # Trimite datele către InfluxDB
    if response.status_code == 204:
        print("Data successfully written to InfluxDB")  # Confirmă scrierea datelor în InfluxDB
    else:
        print(f"Failed to write data to InfluxDB: {response.text}")  # Afișează mesaj de eroare dacă scrierea a eșuat

while True:
    try:
        line = ser.readline().decode('utf-8', errors='ignore').strip()  # Citește o linie de pe portul serial
        print(f"Received from serial: {line}")
        if line.isdigit():  # Verifică dacă linia citită conține doar cifre
            send_to_influxdb(line)  # Trimite datele la InfluxDB
        else:
            print(f"Invalid data received: {line}")  # Afișează un mesaj dacă datele primite sunt invalide
    except UnicodeDecodeError as e:
        print(f"Decode error: {e}")  # Afișează mesajul de eroare în cazul unei erori de decodare
    except Exception as e:
        print(f"An error occurred: {e}")  # Afișează orice altă eroare apărută