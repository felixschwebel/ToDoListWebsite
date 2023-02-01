# ToDoListWebsite
For the project, I used the **Flask** Framework to build a **ToDoList Web application**. I designed and built everything myself. For the styling, I used **Bootstrap**, for the communication with the database **SQLAlchemy** and to structure my HTML files **Jinja-templating**. 

<img width="843" alt="Screenshot 2023-02-01 at 21 06 38" src="https://user-images.githubusercontent.com/111788725/216152060-af21903b-6259-4cc9-9754-9dedbe6dcb69.png">

This application allows the user to sign up for an account and to create multiple to-do lists.

<img width="843" alt="Screenshot 2023-02-01 at 21 06 49" src="https://user-images.githubusercontent.com/111788725/216152305-313bf7cc-6b1c-4357-b03a-29ae29c5d0dd.png">
<img width="842" alt="Screenshot 2023-02-01 at 21 07 03" src="https://user-images.githubusercontent.com/111788725/216152358-e8879a5e-032f-416f-9c94-e9f22c99be2a.png">
<img width="840" alt="Screenshot 2023-02-01 at 21 07 42" src="https://user-images.githubusercontent.com/111788725/216152460-6ad13429-b6ee-4f7a-a654-5617deaa9ef3.png">

When a new list is created, the user can add, delete or check off tasks. 

<img width="841" alt="Screenshot 2023-02-01 at 21 08 13" src="https://user-images.githubusercontent.com/111788725/216152520-dd5f3ad2-8a7c-4431-98a0-98bc90a100f1.png">
<img width="842" alt="Screenshot 2023-02-01 at 21 08 28" src="https://user-images.githubusercontent.com/111788725/216152554-598756cc-4fae-44bf-8ff6-18495f41b92d.png">

I used the ``generate_password_hash``  and ``check_password_hash`` functions from **werkzeug** to secure the user passwords in the database. 

<img width="676" alt="Screenshot 2023-02-01 at 21 11 41" src="https://user-images.githubusercontent.com/111788725/216152753-df2204d8-8078-4a91-b249-5a299fc39e77.png">

To make sure that unauthorized users can't access other pages than the signup and login page I used the ``LoginManager`` from ``flask_login``. 

<img width="334" alt="Screenshot 2023-02-01 at 21 04 25" src="https://user-images.githubusercontent.com/111788725/216151225-3e8f6c74-6dc7-49c8-9fa4-938dcf32c06a.png">

<img width="748" alt="Screenshot 2023-02-01 at 21 05 51" src="https://user-images.githubusercontent.com/111788725/216151470-55926a4e-db7e-4276-9023-057f0d1b864b.png">

To create and access all the forms I used **WTForms**.

<img width="617" alt="Screenshot 2023-02-01 at 21 15 22" src="https://user-images.githubusercontent.com/111788725/216153513-c585e8e3-20fb-456b-8718-fd98e2537d07.png">
