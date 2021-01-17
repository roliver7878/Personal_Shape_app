# PersonalShape app by Rogerio

This project is made to implement a flask app that returns data from a database and executes without breaking.

**Report1** [Report Privacy and Security Analysis](docs/Report_1_Privacy_and_Security_Report.md)

**Report2:** [Report Professional Ethical Legal](docs/Report_2_Professional_Ethical_Legal.md)

My app is a personalshape app.
On PersonalShape, users will be able to:

* register as a user and add their name
* add their details to their profile 
* add a diet program
* see a list of recommended products



**R4, R9:** The Personal Shape app has a **PostgreSQL database** in an AWS EC2 instance. The relationship between tables include one-to-one, one-to-many and many-to-many. I manipulate the database using SQLAlchemy. This module uses an ORM which abstracts table records into Python classes.



## Proposed Entity Relationship Diagram

* Each User can only make one profile. However they can have many programs.
* There is a many to many relationship between products and programs


![Entity_Relationship_Diagram](docs/ERD_diagram.png)


to make changes to the model that will automatically recorded every single time you migrate.