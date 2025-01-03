import socket

ip = '10.10.10.128'

for port in range(1, 100):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)  # Timeout süresi 1 saniye olarak ayarlandı

    try:
        s.connect((ip, port))
        print(f"Port {port}: open")
    except Exception as e:
        print(f"Port {port}: closed")
    finally:
        s.close()
