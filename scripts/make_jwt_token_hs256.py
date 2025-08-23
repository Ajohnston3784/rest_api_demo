import jwt
import time

print(jwt.encode({
  "sub":"user_123","tenant_id":"acme-co","roles":["manager"],
  "iss":"https://auth.example.com","aud":"quotes-api","exp":int(time.time())+3600
}, "change-me-demo-secret", algorithm="HS256"))