# Ramen

 
## Technologies Used
- **Frontend**: 
  - React
  - HTML5
  - CSS3

- **Backend**: 
  - FastAPI
  - Python
  - MySQL (for database management)

- **Deployment**: 
  - GitHub (for version control)

### Frontend Setup
1. Clone the repository:
   git clone https://github.com/Amyliamg/Ramen.git
2. Navigate to Frontend:
   cd /Frontend
3. Install all the dependencies:
   npm install
4. Start the React development server:
   npm start
5. It will run at http://localhost:3000


### Backend Setup
1. Navigate to the backend directory:
   cd Ramen/Backend
2. Install the required packages:
    pip install -r requirements.txt
3. Create a new database for the project and store your host authentication in .env
4. Run the database migration scripts (Backend/createdb.py) [it will automatically create a sql_ramen database with three tables]
5. Run backend  
   uvicorn main:app --reload
6. It will run at http://localhost:8000

(use the following comment to set up virtual env )
  python -m venv myenv
  os:source myenv/bin/activate
  window:myenv\Scripts\activate
 
