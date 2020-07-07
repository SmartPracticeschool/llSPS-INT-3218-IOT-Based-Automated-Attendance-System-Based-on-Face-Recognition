import requests

r=requests.get('https://www.fast2sms.com/dev/bulk?authorization=lfBwdoqVEMsGYPaKhk517J9InvytCpTujQH4DgeFxZ3LRm8ASUUdM6zjECX1GubLtyivqHIZ8Bf9gKPa
               &sender_id=FSTSMS&message=This message is to inform you that your child did not come to college today&language=english&route=p
               &numbers=9398659128,6304514195,9676926774,9381274122')

print(r.status_code)
