
1. Create a self-signed cert (.CRT) and private key (.KEY) by following these clutch instructions:
https://stackoverflow.com/questions/37959644/generate-ssl-key-and-cert-in-windows

Install OpenSSL from: https://slproweb.com/products/Win32OpenSSL.html
And run the following commands:

openssl genrsa -des3 -out server.key 2048
openssl rsa -in server.key -out server.key
openssl req -sha256 -new -key server.key -out server.csr -subj "/CN=localhost"
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt

2. 