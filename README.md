<div id="top"></div>

<!-- ABOUT THE PROJECT -->
## About The Project

This Python Rest API aims to satisfy the requirements listed in a list of requirements defined under a case study PDF.
Basicly the rest api has to: 
* Run an endpoint that operates CRUD operations for authors
* Run an endpoint that operates CRUD operations for categories
* Run an endpoint that operates CRUD operations for blogs


### Built With

This project is built on Microsoft Visual Studio Code.  

### Prerequisites

Before continue, make sure you installed docker on your machine. To download docker [click here](https://www.docker.com/products/docker-desktop). 
To run integration tests, it is highly recommended to install dotnet on your machine.


### Installation and Docker Run

Open the terminal(cmd) and write each line to run program on docker

1. Clone the repo
   ```sh
   git clone https://github.com/yemlihaoner/PythonRestAPI.git
   ```
2. Change repository to run endpoints on docker
   ```sh
   cd ./PythonRestAPI
   ```
3. Run docker-compose to activate webapi and database. If error occures related to db generation, Stop docker by CTRL+C and re-run command.
   ```sh
   docker-compose up
   ```

### Warning

In order to upload files to cloud, you will need to set a .env file with required information:
* CLOUD_NAME='cloud_name'
* API_KEY='api_key'
* API_SECRET='api_secret'

In this project, [@cloudinary](https://cloudinary.com/) is used in order to save files in cloud.
If you dont have an account click the [@link](https://cloudinary.com/) and register for free to access api keys.




### How to send request

After running the program on the docker, you can use api from http://localhost:80. Available api endpoints:

For Author:
* [GET] http://localhost:80/author -> Gets all author records
* [GET] http://localhost:80/author/{id-number} -> Gets spesific author record for given id
* [DELETE] http://localhost:80/author/{id-number}  -> Deletes spesific author record for given id if author.blog_amount is equal to 0
* [POST] http://localhost:80/author  -> Creates a new author record
* [PUT] http://localhost:80/author/{id-number} -> Updates the author record for given id
!POST and PUT requests require a JSON in Request Body in format below: 
```json
{
    "first_name": "name",
    "last_name": "last name"
}
```
For Category:
* [GET] http://localhost:80/category -> Gets all category records
* [GET] http://localhost:80/category/{id-number} -> Gets spesific category record for given id
* [DELETE] http://localhost:80/category/{id-number}  -> Deletes spesific category record for given id if there is no blog recorded with its id
* [POST] http://localhost:80/category  -> Creates a new category record
* [PUT] http://localhost:80/category/{id-number} -> Updates the category record for given id
!POST and PUT requests require a JSON in Request Body in format below: 
```json
{
    "name":"name",
    "description":"description"
}
```
For Blog:
* [GET] http://localhost:80/blog -> Gets all blog records
* [GET] http://localhost:80/blog/{id-number} -> Gets spesific blog record for given id
* [DELETE] http://localhost:80/blog/{id-number}  -> Deletes spesific blog record for given id and updates related authors blog numbers
* [POST] http://localhost:80/blog  -> Creates a new blog record
* [PUT] http://localhost:80/blog/{id-number} -> Updates the blog record for given id
!POST and PUT requests require a from-data in Request Body in format below: 

| Key               | Value             |
|-------------------|-------------------|
| title             | string(40)        |
| content           | string(200)       |
| image             | - select file -   |
| tags              | string(200)       |
| category          | integer           |
| author            | integer           |

Output format for Blog:
```json
[
    {
        "author": 1,
        "category": 1,
        "content": "12",
        "date_created": "Sun, 21 Nov 2021 19:42:53 GMT",
        "id": 1,
        "image": "https://res.cloudinary.com/yemliha/image/upload/v1637523773/lk278b28ejbp9pjjtspk.png",
        "tags": "22-23",
        "title": "12"
    }
]
```

<!-- CONTACT -->
## Contact

Ahmet Yemliha Öner - [@github](https://github.com/yemlihaoner) - [@website](https://yemlihaoner.github.io) - a.yemlihaoner@gmail.com

Project Link: [https://github.com/yemlihaoner/PythonRestAPI](https://github.com/yemlihaoner/PythonRestAPI)

<p align="right">(<a href="#top">back to top</a>)</p>
