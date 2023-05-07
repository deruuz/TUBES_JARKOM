#mengimport module socket
from socket import * 
#Menginisialisasi alamat dan nomor port untuk server
SERVER_ADDRESS = (HOST, PORT) = '0.0.0.0', 8888 
#Menentukan ukuran antrian permintaan maksimum yang diterima oleh server
REQUEST_QUEUE_SIZE = 5
#Direktori tempat berkas-berkas website disimpan
FILE_DIRECTORY = 'file'

#Menerima kode status HTTP dan mengembalikan string yang berisi header HTTP
def http_header(code) -> str:
	if code == 200:
		header = "HTTP/1.1 200 OK\n"
	elif code == 404:
		header = "HTTP/1.1 404 Page not found\n"

	header += "Server:Kelompok 8 Web Server\n"
	header += "Connection: Alive\n\n"
	return header

def handle_request(client_connection:socket):
	request = client_connection.recv(1024)
	data = bytes.decode(request)
	print(data)

	if len(data.split()) > 0:
		method = data.split()[0]
		print("data split 0",method)

		if method == 'GET' or method == 'HEAD':
			resource = data.split()[1]
			print("data split 1",resource)
			resource = resource.split('?')[0]
			print("resource split ?",resource.split('?'))

			if resource == '/':
				resource = 'file\\index.html'

			resource = FILE_DIRECTORY + resource

			header, body = create_respon(resource)
			http_response = header.encode()
			if method == "GET":
				http_response += body
			client_connection.sendall(http_response)
			print("HTTP Response: " + str(http_response) + "\n")

def create_respon(FILE_NAME):
	try:
		file = open(FILE_NAME, 'rb')
		body = file.read()
		file.close()
		header = http_header(200)
	except Exception as e:
		print("Page not found" + str(e))
		header = http_header(404)

		file = open('file\\error.html', 'rb')
		body = file.read()
		file.close()
		header = http_header(404)
	return header, body

def serve_forever():
	listen_socket = socket(AF_INET, SOCK_STREAM)
	listen_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

	try:
		listen_socket.bind(SERVER_ADDRESS)
	except error as err:
		print("Bind failed. " + str(err))

	listen_socket.listen(REQUEST_QUEUE_SIZE)

	print("HTTP Sever running on port %s \n" % PORT)

	while True:
		client_connection, client_address = listen_socket.accept()
		handle_request(client_connection)
		client_connection.close()

#Memanggil fungsi utama serve_forever() untuk menjalankan server
if __name__ == '__main__':
	serve_forever()
