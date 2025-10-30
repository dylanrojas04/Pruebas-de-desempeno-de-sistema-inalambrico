# === RX con visualización de potencia y data rate ===
from machine import Pin, SPI, I2C, PWM
from nrf24l01 import NRF24L01, POWER_0, POWER_1, POWER_2, POWER_3, SPEED_250K, SPEED_1M, SPEED_2M
from ssd1306 import SSD1306_I2C
import utime

# --- Configuración SPI ---
spi = SPI(0, sck=Pin(6), mosi=Pin(7), miso=Pin(4))
csn = Pin(15, Pin.OUT)
ce = Pin(14, Pin.OUT)

# --- NRF24L01 ---
nrf = NRF24L01(spi, csn, ce, channel=90, payload_size=32)
nrf.set_power_speed(POWER_1, SPEED_250K)                                 # PARAMETROS A CONFIGURAR
nrf.open_tx_pipe(b'\xd2\xf0\xf0\xf0\xf0')  # Dirección inversa
nrf.open_rx_pipe(1, b'\xe1\xf0\xf0\xf0\xf0')
nrf.start_listening()

# --- OLED ---
i2c = I2C(1, scl=Pin(11), sda=Pin(10))
oled = SSD1306_I2C(128, 64, i2c)
oled.fill(0)
oled.text("RX listo...", 25, 0)
oled.text("Esperando datos...", 0, 20)
oled.show()

# --- Servo ---
servo = PWM(Pin(0))
servo.freq(50)  # 50 Hz típico de servos RC

def set_angle(angle):
    duty = int((angle / 180) * 6553 + 1638)
    servo.duty_u16(duty)

# --- Variables para mostrar configuración ---
potencia_actual = "0 dBm"                           #----CONFIGURAR DEPENDE DE LA OPCION ELEGIDA
tasa_actual = "1 Mbps"

print("🟢 Receptor listo. Esperando datos del TX...")

# --- Bucle principal ---
while True:
    if nrf.any():
        msg = nrf.recv()
        texto = msg.decode('utf-8', 'ignore').replace('\x00', '').strip()
        print("📩 Recibido:", texto)

        if texto.startswith("ACC,"):
            try:
                partes = texto.split(",")
                ax = float(partes[1])
                ay = float(partes[2])
                az = float(partes[3])
                angulo = int(partes[5]) if len(partes) > 5 else 90

                # Si el mensaje contiene info de configuración (opcional)
                if len(partes) > 7:
                    potencia_actual = partes[6]
                    tasa_actual = partes[7]

                # Actualizar servo
                set_angle(angulo)

                # Mostrar en OLED
                oled.fill(0)
               # oled.text("📡 RX - Datos:", 0, 0)
                oled.text(f"Ax: {ax:.2f}", 0, 0)
                oled.text(f"Ay: {ay:.2f}", 0, 15)
                oled.text(f"Az: {az:.2f}", 0, 25)
                oled.text(f"Servo: {angulo}°", 0, 35)
                oled.text(f"Pwr:{potencia_actual}", 0, 45)
                oled.text(f"Rate:{tasa_actual}", 0, 55)
                oled.show()

            except Exception as e:
                print("⚠️ Error procesando:", e)
                oled.fill(0)
                oled.text("⚠️ Error al leer", 0, 25)
                oled.show()

    utime.sleep(0.01)
