step 1 :- Install docker in the local machine
step 2 :- RUN docker-compose build
step 3 :- RUN docker-compose up -d
step 4 :- Wait 5 min and check the pgadmin4, database, api docker logs 
          completly loaded
step 5 :- Add pgadmin4 username and password in env file
step 6 :- Go to pgadmin4 the following url http://localhost:8004/
step 7 :- create server using docker container container name or sevice name. 
          If the server created database automatically created.
