
# What is this?

This is a stand alone example of a client-service and auth-service that uses the
[drf_remotejwt](https://github.com/garrethcain/drf_remotejwt) package to 
authenticate a user logging into a client-service against a remote auth-service.
This is most useful in a microservice type set up.
Most useful if you're building a microservice ecosystem and want all services
to authenticate against a centralised authentication-service.


At a high level, it works like this;

1. Admin or a Signup mechanism create's a user in the auth-service.
2. User logs in at the µService (auth request is proxied to auth-service to 
   retrieve and then create or update a local instance of the user)
3. Try access µService endpoint;
   1. µService checks with auth-service/auth/token/verify that this token is 
     valid;
   2. µService takes the JWT and decodes it to get the user_id (we can trust it 
     because it was verified to be untampered with by `/token/verify/`);
   3. Take the user_id and check for a local user object;
      1. If exists, instatiates and use.
      2. If not exists, requests `auth-service/auth/users/{user-id-from-jwt}/`
         1. Creates a local user object from that one returned. (Details should be 
         updated when authing the first time.)
         2. Instatiates and uses.

The caveat is that a users personal details in the client-service won't update 
until they log out and back in again. Fields are also likely to be overwritten
at login time. So the local services user object should be considered ephemeral.

There is no need to customise the JWT claim, because it should only contain a 
user_id by design, permissions will be created when the user object is created 
or updated at login in the client-service. It doesn't make sense for the 
auth-service to keep track of remote service permissions.

    

# Standing up the Auth-Service:

Enter the auth-service directory: `cd auth-service`

Create a virtual environment; `virtualenv .venv` then activate it; 
`source .venv/bin/activate`

You should see;
```
(.venv)  username@domain-local  ~/auth-client-service-example/auth-service 
```

```
pip install -r requirements.txt
```

The auth-service needs to have a completely clean database for this to work
reliably, as a test example, so be sure to `python manage.py flush` or 
`python manage.py migrate` depending on where you're up to.

In the auth-service, create three test users as below.
* admin | admin@test.com | admin-pass
* staff | staff@test.com | staff-pass
* user | user@test.com | user-pass

Eg. 
```
export DJANGO_SUPERUSER_EMAIL=admin@test.com
export DJANGO_SUPERUSER_USERNAME=admin
export DJANGO_SUPERUSER_PASSWORD=admin-pass
python manage.py createsuperuser --noinput
```
or
```
python manage.py createsuperuser
```
Then stand up the auth-service and log into `http://127.0.0.1:8000/admin/` and
create the other two users, setting `is_staff=True` for the staff user.


For this example we're going to assume that the auth-service is running at 
`:8000` and the client service is running at `:8001`, by doing this you should 
be able to copy/paste the configuration further down.

Run the auth-service;
```
python manage.py runserver 0.0.0.0 8000
```

Leave this to idle away in it's own terminal window to one side for now. Next
we'll start the client-service.


# Standing up the Client-Service

Set the API's authentication for DRF.

Let's create a fresh db.

Enter the services directory `cd client-service` then migrate 
`python manage.py migrate`

You should have a completely fresh database now with no users.

# Let's test.

This shoud still be running from earlier, however, in the auth-service
directory;
`python manage.py runserver 127.0.0.1 8000`

in the client directory:
`python manage.py runserver 127.0.0.1 8001`

Now that both services are up;

1. Visit http://127.0.0.1:8000/auth/token/
2. Login with the above user, not the admin.
3. Copy the access_token and run the below;

Step "2" is the user@test.com user.

`export ACCESS_TOKEN={PASTE_TOKEN_HERE}`

`curl \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  http://localhost:8001/api/test/`

It should return the user from the auth-service the first time and the second 
time it will return the user from the local db. You can confirm this by updating
the user in the auth-service after the first request.

Users should only be updated when logging into the client-service; currently not
supported.

---

# How to test the API

In the below examples we're mking requests to simple super simple API 
(client-service) which will reach out to the auth-service to retrieve, verify,
and refresh the user.
If you check the db.sqlite3 databse before making any requests the `user` table
will be empty. After making a few successful requests there will be some users.

Remember the users added to the auth-service further back when three users
were added. You'll need those email and passwords shortly.
Also remember that the auth-service is at `:8000` and the client-service is at
`:8001`. As a client-service user, we should never interact with the 
auth-service directly. It shouldn't even be accessible to the public.

Then follow the example requests below.

## Authorise and obtain a token pair

`curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"email": "user@test.com", "password": "user-pass"}' \
  http://127.0.0.1:8001/auth/token/`


## Perform a generic API requst
 Should return 'success'.

`curl \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  http://127.0.0.1:8001/api/test/`


## Refresh an expired token

`curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"refresh": "${REFRESH_TOKEN"}}' \
  http://127.0.0.1:8001/auth/token/refresh/`


## Verify the token is correct
 Performed by the client-service with every single JWT API request.

`curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"token": "${REFRESH_TOKEN}"}' \
  http://127.0.0.1:8001/auth/token/verify/`


## Get the user details
 This would be done inside the Auth handler when the user doesn't exist.

`curl \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  http://localhost:8001/auth/users/{user_id}/`



## TODO:

1. Create signup, password reset etc endpoints.
2. Improve exception handling.
3. Login logic in client-service.
4. Provide a way for an admin to add a user into a service before the user logs 
  in.
5. Clean up exception words.