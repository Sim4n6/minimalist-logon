# minimalist-logon
A minimalist website with logon and logout support using Python 3.x and Flask.

#### Features:
 - minimalistic
 - logon/logout support **not secure, it is on its early stage**
 - written in Python using Flask and Sqlite3
 
#### TODOs : 
 - [ ] not use one single hash and salt it 
 - [ ] use a dedicated module : passlib, etc.
   
INSTALL
----
 Clone the repository from github : 

    $ git clone https://github.com/Sim4n6/minimalist-logon.git minimalist-logon
    $ cd minimalist-logon

Create a virtual environnement on linux : 

    $ python3 -m venv venv
    $ source venv/bin/activate
    
Create a virtual environnement on windows :

    $ python3 -m venv venv
    $ venv\Scripts\activate.bat
    
Install the necessary packages including Flask and Pytest: 
    
    $ pip3 install -r requirements.txt
   
Run
---
On linux :

    $ python minimalist-logon.py

On Windows :

    > python minimalist-logon.py

Open http://127.0.0.1:5000 in a browser.

