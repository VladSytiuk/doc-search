Doc-search


### Description: 
Doc-search is a gpt-3.5-turbo based application where users can upload their pdf or md 
documents and ask questions related to these documents. Each user has a separate scope 
with their documents that are saved in vector store and only they have access to them. 
The application also implements a key system, by which a user can upload 
up to 10 documents per day and ask no more than 10 questions per minute. 
The graphql api is used to interact with the application.


## Installation:

Clone the project and then go to the root directory and create .env file like in .env.example 
(You might want to change the credentials). Then you can install app via docker-compose:


```commandline
docker-compose up --build
```
## Usage:

GraphQL api is available on this endpoint: http://127.0.0.1:8000/graphql#

After sign up you should pass JWT token in headers like this:

```commandline
{
  "headers":{
    "Authorization": "JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IlZsYWRpc2xhdnIiLCJleHAiOjE2OTU5MTE3MzMsIm9yaWdJYXQiOjE2OTU4ODE3MzN9.O_6nWir8WWId64J5PaTk_pb6hek-ydCKVeBfDDmWcEE"
  }
}
```