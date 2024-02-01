**HRMS Backend**

To install and run the project follow the instruction below.

1. Clone the repository using `git clone`
2. Set up a database in `PostgreSQL`
3. Create a new file called `.env` in the project root and fill it as shown in `.env.example`.
4. Install the requirements `pip install -r requirements.txt`
5. Load roles/operations/resources data `python manage.py loaddata initial_data.json`
6. Run the project `python manage.py runserver`
