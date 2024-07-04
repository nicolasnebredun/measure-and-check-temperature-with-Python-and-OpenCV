import http.client
import json

conn = http.client.HTTPConnection("10.1.1.26", 8182)

payload = json.dumps({
        "args": {
        "to": "5569992692250@c.us",
        "content": "ATENÇÃO: Servidor com temperatura acima do normal!"
        }
        })
headers = {
        'Content-Type': 'application/json'
        }
conn.request("POST", "/eagle-session/sendText", payload, headers)
res = conn.getresponse()
data = res.read()
print('Mensagem Enviada')
#print(data.decode("utf-8"))