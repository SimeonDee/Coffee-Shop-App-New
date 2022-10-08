----
- <span style='color:brown;'>Contributor:</span> `Adedoyin Simeon Adeyemi` <br />
- <span style='color:brown;'>Version:</span> `v1.0`

-----

# Auth0 Authentication System API Endpoints
---

## Login

For login into Auth0. Form your link using this format 

- Method: ***`GET`*** 
```url 
https://{DOMAIN}/authorize?audience={AUDIENCE}&response_type=token&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URL}
```

## Logout

For logout of Auth0. Form your link using this format 

- Method: ***`GET`*** 
```url 
https://{DOMAIN}/v2/logout?client_id={CLIENT_ID}&returnTo={REDIRECT_LOGOUT_URL}
```
