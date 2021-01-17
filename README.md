This project is made to implement a flask app that returns data from a database and executes without breaking.

R2: Report 1: Privacy and Security Analysis

R3: Report 2 Professional Ethical Legal

My app is designed to be similar to LinkedIn but for IT professionals. On ConnectIT, IT professionals will be able to:

register as a user and add photos
like and comment on user posts
add work history, study history, certifications and links to their resume/projects
write down meetings they have
send messages to other users and like their messages
Docs for my app:

Trello board for project management
End points for interacting with the flask app
Wireframes for designing the front end
R4, R9: My data model uses a PostgreSQL database and has one-to-one, one-to-many and many-to-many relationships between the tables. The application is able to communicate with the postgresql database in the cloud by using SQLAlchemy. This module uses Object Relational Mapping which abstracts table records into Python classes. The application also makes use of Marshmallow schemas to validate data sent to the database and to deserialise into json format before being sent back to the user in the HTTP response.

R7: An example of an API endpoint aggregating data is below. This endpoint gets the number of likes for a post. This can be done by counting the number of distinct users who like a post.

get_num_likes_example

R6: User-interface using Jinja
URL: http://127.0.0.1:5000/web/login
Login Page
jinja_log_in_page

List of work experiences
jinja_work_experiences

R11: Join table example
join_table_example

Proposed Entity Relationship Diagram
Each User can have multiple images, certifications, work histories, connections, meetings, messages, study histories, resume/projects, posts, comments and like multiple posts
Each Like belongs to one post and one user
Each comment belongs to one post and one user
Each connection has one user who requests the connection and one user who can decide to confirm it
