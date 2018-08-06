
### 配置抓包
----

Fiddler :
    
    Tools->Options->HTTPS-> Decrypt HTTPS traffic √  ...from all processes
    
    notice Tools->Options->Connections->port
    
    Tools->Options->HTTPS->Export Root Certificate To Desktop
    
    convert cert to pem
    
    openssl x509 -inform der -in C:\Users\xxx\Desktop\FiddlerRoot.cer  -out C:\Users\xxx\Desktop\FiddlerRoot.pem
    
 
Python request:
    
    with 
    
    proxies={'http': 'http://127.0.0.1:8888', 'https': 'http://127.0.0.1:8888'}
    ,verify=r"C:\Users\xxx\Desktop\FiddlerRoot.pem"
    