# mengimport module socket
from socket import *
# import module os untuk konfigurasi path
import os

# Menginisialisasi alamat dan nomor port untuk server
SERVER_ADDRESS = (HOST, PORT) = 'localhost', 8888
# Menentukan ukuran antrian permintaan maksimum yang diterima oleh server
REQUEST_QUEUE_SIZE = 5
# Direktori tempat berkas-berkas website disimpan
FILE_DIRECTORY = os.path.join(os.path.dirname(__file__), "file")

# Menerima kode status HTTP dan mengembalikan string yang berisi header HTTP
def http_header(code) -> str:  # mengembalikan string
    if code == 200:  # jika kode 200 maka kembalikan 200 OK
        header = "HTTP/1.1 200 OK\n"  # mengembalikan 200 OK
    elif code == 404:  # jika kode 404 maka kembalikan 404 Page not found
        header = "HTTP/1.1 404 Page not found\n"  # mengembalikan 404 Page not found

    header += "Server:Kelompok 8 Web Server\n"  # menambahkan server: kelompok 8 web server
    header += "Connection: keep-alive\n\n"  # menambahkan connection: keep-alive
    return header  # mengembalikan header

def handle_request(client_connection: socket):  # menerima koneksi dari client
    request = client_connection.recv(1024)  # menerima request dari client
    data = bytes.decode(request)  # mendecode request dari client
    print(data)  # menampilkan request dari client

    if len(data.split()) > 0:  # jika panjang data split lebih dari 0
        method = data.split()[0]  # mengambil method dari data split
        print("data split 0", method)  # menampilkan method dari data split

        if method == 'GET' or method == 'HEAD':  # jika method GET atau HEAD
            resource = data.split()[1]  # mengambil path yang dicari dari client
            print("data split 1", resource)  # menampilkan resource dari data split
            resource = resource.split('?')[0]  # memotong path resource sehingga tersisa hanya nama file saja
            print("resource split ?", resource.split('?'))  # menampilkan resource dari data split

            if resource == '/':  # jika resource sama dengan /
                resource = '/index.html'  # maka resource sama dengan file\index.html

            resource = os.path.join(FILE_DIRECTORY, resource[1:])  # resource sama dengan file directory + resource
            print("resource ", resource)
            header, body = create_respon(resource)  # membuat response dari resource
            http_response = header.encode()  # mengencode header
            if method == "GET":  # jika method GET
                http_response += body  # mengencode body
            client_connection.sendall(http_response)  # mengirim http response
            print("HTTP Response: " + str(http_response) + "\n")  # menampilkan http response


def create_respon(FILE_NAME):
    # membuat response dari filename, jika file tidak ditemukan maka kembalikan 404 dan halaman not found
    try:
        file = open(FILE_NAME, 'rb')  # membuka file
        body = file.read()  # membaca file
        file.close()  # menutup file
        header = http_header(200)  # mengembalikan 200 OK
    except Exception as e:  # jika terjadi exception
        print("Page not found" + str(e))  # menampilkan page not found

        file = open(os.path.join('file', 'error.html'), 'rb')  # membuka file error.html
        body = file.read()  # membaca file error.html
        file.close()  # menutup file error.html
        header = http_header(404)  # mengembalikan 404 Page not found
    return header, body  # mengembalikan header dan body


def serve_forever():  # fungsi utama untuk menjalankan server
    listen_socket = socket(AF_INET, SOCK_STREAM)  # membuat socket
    listen_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # mengatur socket

    try:  # mencoba untuk menjalankan server
        listen_socket.bind(SERVER_ADDRESS)  # mengikat socket ke alamat server
    except error as err:  # jika terjadi error
        print("Bind failed. " + str(err))  # menampilkan bind failed

    listen_socket.listen(REQUEST_QUEUE_SIZE)  # mendengarkan koneksi dari client

    print("HTTP Sever running on port %s \n" % PORT)  # menampilkan HTTP Server running on port 8888

    while True:  # selama true
        client_connection, client_address = listen_socket.accept()  # menerima koneksi dari client
        handle_request(client_connection)  # menangani request dari client
        client_connection.close()  # menutup koneksi dari client


# Memanggil fungsi utama serve_forever() untuk menjalankan server
if __name__ == '__main__':
    serve_forever()  # memanggil fungsi serve_forever() untuk menjalankan server
