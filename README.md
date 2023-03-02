# Veo-Assignment


## Introduction
This is an assignment for the full stack position in Veo. The assignment is to implement a tree structure using Django Framework.
And for the visualisation of the tree, I have used React.


## Back-end Assumptions
1. No authentication/authorazation is required for the API.
2. A default tree is already present in the database.
3. A root node does not have any parent.
4. Only one root node is present in the database.
5. The methods implemented for the tree are not optimized for performance and work on the assumption that the tree is not too large.
6. 16 test cases are written for the API but it may not cover all the cases.
7. The docs are auto generated using drf-yasg. You can find them at http://localhost:8000/docs

## Back-end Technologies Used
* Django
* Python 3.10
* Django Rest Framework
* drf-yasg
* corseheaders
* db.sqlite3
* docker

## Front-end Assumptions
1. The frontend assumes that at least one node already exists in the database 
2. The tree is small otherwise it won't fit in the screen. 
3. The only operation that can be done besides displaying the company tree 
is to create a node after you have selected a node. 
4. This ui app is not well tested. 


## Front-end Technologies Used
* React
* Typescript
* React-query
* bootstrap
* Node 18
* npm
* docker


## Running the apps
You can either see the readme in the backend and frontend folder or follow the steps below.

### Running the backend using docker
In the project directory, you can run (assuming you have docker installed and running linux):
```
sudo docker build  . -t veo-backend
sudo docker run -p 8000:8000 veo-backend
``` 
Runs the app in the development mode.\
Open [http://localhost:8000/api/v1/tree](http://localhost:8000/api/v1/tree) to view it in the browser.

### Running the frontend using docker
In the project directory, you can run:
```
sudo docker build  . -t veo-frontend
sudo docker run -p 3005:3005 veo-frontend
```
Runs the app in the development mode.\
Open [http://localhost:3005](http://localhost:3005) to view it in the browser.


### Available Endpoints
* **/api/v1/tree/** - GET - Returns the tree in JSON format
* **/api/v1/nodes/{id}** - GET, POST - Returns the node with the given id in JSON format. POST request can be used to create a new node with a parent with id={id}.
* **/api/v1/nodes/{id}/update** - PATCH - Updates the node with the given id. The request body should contain the parent_id to update the parent of the current node ({id}).


## Author 
**Stelios (Stylianos) Bitzas - Full Stack Developer**






















