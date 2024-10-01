I am currently building a fullstack version control application with FastAPI and React

### How to run the project locally
Clone the project and open it
```bash
git clone [this projects link]
cd VersionArchive
```
Download the required python packages
```
pip install -r backend/requirements.txt
```
Download the required npm packages
```bash
npm install --prefix frontend
```

#### Run the project
Run backend
```bash
python3 -m uvicorn backend.app.main:app --reload
```
In a different terminal run the frontend
```bash
npm run dev --prefix frontend
```