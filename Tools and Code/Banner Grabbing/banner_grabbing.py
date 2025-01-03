import socket

ip = '10.10.10.128'

for port in range(1, 100):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)
    
    try:
        s.connect((ip, port))
        response = s.recv(1024)

        # Port açık ve yanıt alındıysa
        print(f"{port}: open : Banner : {response.decode()}")

    except socket.timeout as t:
        if port == 80:
            # HTTP portu olduğunda farklı bir istek gönderelim
            httpMessage = "GET / HTTP/1.0\r\n\r\n"
            s.send(httpMessage.encode())
            httpRcv = s.recv(1024)
            print(f"{port}: open : Banner : {httpRcv.decode()}")
        else:
            print(f"{port}: timed out - use different method")

    except Exception as e:
        # Diğer hatalar için port kapalı olabilir
        # print(f"{port}: closed : reason: {str(e)}")
        pass

    finally:
        s.close()
