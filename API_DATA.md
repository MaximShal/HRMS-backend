### Registration:

api/v1/register/

```JSON
{
  "email": "example@noreply.com",
  "password": "Password",
  "password_confirm": "Confirm Password",
  "company_name": "Company Name"
}
```
```
{
    "message": "User was successfully created"
}
```
```
{
    "email": [
        "user with this email already exists."
    ]
}
```
```
{
    "email": [
        "Enter a valid email address."
    ]
}
```
```
{
    "non_field_errors": [
        "This password is too short. It must contain at least 8 characters."
    ]
}
```
```
{
    "non_field_errors": [
        "Check the password"
    ]
}
```
```
{
    "field": [
        "This field may not be blank."
    ]
}
```

### Auth

api/v1/token/

```JSON
{
    "email": "example@noreply.com",
    "password": "Password"
}
```
```
{
    "refresh": "eyJhbGI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwNTUwNjc0MCwiaWF0CexampleAOKl5U8WdA",
    "access": "eyJhbGciOiJIUzI1NiIsInJ9.eyJ0b2tlblexampleMDNDYyNjJhMGEwidXNlcl9pZCI6N30.8WQKMKUw0iJiUnwJGJ9dfTq8VaMUo"
}
```
```
{
    "detail": "No active account found with the given credentials"
}
```

### Refresh 

api/v1/token/refresh/

```JSON
{
    "refresh": "eyJhbGciOiJJ9.eyJ0b2tl1NDIwMzQwLCJqddkNjexampleVzZXJfaWQiOjd9.iRHVau-sz8AhkMKW128DLKTqm_d5WZa4mAOKl5U8WdA"
}
```
```
{
    "access": "eyJhbGciOiJIUzI1NiIsXVCJ9.eyJ0b2tlxYzdiOGU1MzQ2MexamplewIiwidXNlcl9pZCI6N30.jFNLQSe33MzP3DeJ3__rr4knQZpnmQR4z_7MXqrpbUY"
}
```
```
{
    "detail": "Token is invalid or expired",
    "code": "token_not_valid"
}
```
### Verify token

api/v1/token/verify/

```JSON
{
    "token": "eyJhbGciOiJIexampleI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWN4NmsyxzeSvQM64WgnA"
}
```
Response 200 `{}` or 401
```
{
    "detail": "Token is invalid or expired",
    "code": "token_not_valid"
}
```