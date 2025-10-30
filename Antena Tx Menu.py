# === TX con menú de configuración ===
from machine import Pin, SPI, I2C, ADC
from nrf24l01 import NRF24L01, POWER_0, POWER_1, POWER_2, POWER_3, SPEED_250K, SPEED_1M, SPEED_2M
import utime

# --- Configuración SPI ---
spi = SPI(0, sck=Pin(6), mosi=Pin(7), miso=Pin(4))
csn = Pin(15, Pin.OUT)
ce = Pin(14, Pin.OUT)

# --- Menú de configuración ---
print("===== CONFIGURACIÓN TX =====")
print("Seleccione potencia de transmisión:")
print("0: -18 dBm  |  1: -12 dBm  |  2: -6 dBm  |  3: 0 dBm")
p = int(input("Ingrese opción (0–3): ") or 3)

print("\nSeleccione tasa de datos:")
print("0: 250 kbps  |  1: 1 Mbps  |  2: 2 Mbps")
r = int(input("Ingrese opción (0–2): ") or 1)

# --- Asignar potencia ---
if p == 0:
    power = POWER_0
elif p == 1:
    power = POWER_1
elif p == 2:
    power = POWER_2
else:
    power = POWER_3

# --- Asignar data rate ---
if r == 0:
    speed = SPEED_250K
elif r == 1:
    speed = SPEED_1M
else:
    speed = SPEED_2M

print(f"\nPotencia seleccionada: {p}  |  Data rate: {r}")

# --- Inicializar NRF24L01 ---
nrf = NRF24L01(spi, csn, ce, channel=90, payload_size=32)
nrf.set_power_speed(power, speed)

nrf.open_tx_pipe(b'\xe1\xf0\xf0\xf0\xf0')
nrf.open_rx_pipe(1, b'\xd2\xf0\xf0\xf0\xf0')

# --- I2C (MPU6050) ---
i2c = I2C(0, scl=Pin(13), sda=Pin(12))
MPU_ADDR = 0x68
i2c.writeto_mem(MPU_ADDR, 0x6B, b'\x00')

def read_word(reg):
    high = i2c.readfrom_mem(MPU_ADDR, reg, 1)[0]
    low = i2c.readfrom_mem(MPU_ADDR, reg + 1, 1)[0]
    value = (high << 8) | low
    if value >= 0x8000:
        value = -((65535 - value) + 1)
    return value

def read_accel():
    ax = read_word(0x3B) / 16384.0
    ay = read_word(0x3D) / 16384.0
    az = read_word(0x3F) / 16384.0
    return ax, ay, az

# --- Joystick ---
xAxis = ADC(Pin(27))
yAxis = ADC(Pin(26))

print("\n🚀 Transmisor listo. Enviando datos cada 100 ms...")

while True:
    try:
        ax, ay, az = read_accel()
        x_val = xAxis.read_u16()
        angulo = int((x_val / 65535) * 180)
        angulo = max(0, min(180, angulo))
        mensaje = f"ACC,{ax:.2f},{ay:.2f},{az:.2f},SERVO,{angulo}"
        nrf.send(mensaje.encode())
        print("📤 Enviado:", mensaje)
    except OSError:
        print("⚠️ Error al enviar datos (NRF no responde)")
    utime.sleep(0.1)
