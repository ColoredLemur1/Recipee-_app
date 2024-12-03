from app import app,db
import sys

path = '/home/colorfast/Documents/web_application/coursework2_web/run.py'
if path not in sys.path:
   sys.path.insert(0, path)

if __name__=="__main__":
    db.create_all()
    app.run(debug=True)