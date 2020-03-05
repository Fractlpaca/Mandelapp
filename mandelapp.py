"""Hopefully, this will allow users to save their snips in a SQLite database
Created by Joseph Grace
Last edited 04/02/2020"""

import os
from flask import Flask,request,redirect,render_template,url_for,session
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt

project_dir = os.path.dirname(os.path.abspath(__file__) ) #This is the directory of the project
database_file = "sqlite:///{}".format(os.path.join(project_dir,"database.db")) #Get path to database file

app = Flask(__name__) #define app
app.config["SQLALCHEMY_DATABASE_URI"] = database_file #give path of database to app
app.config["thumbnails"] = "./static/thumbnails"
app.secret_key="dyhu327eof9u,./pkdfsoiw"
db = SQLAlchemy(app) #connect to database

class Locations(db.Model):
    loc_id = db.Column(db.Integer(), unique=True, nullable=False, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False, default="Untitled")
    x = db.Column(db.Float(), nullable=False, default=0)
    y = db.Column(db.Float(), nullable=False, default=0)
    zoom = db.Column(db.Float(), nullable=False, default=1)
    limit = db.Column(db.Integer(), nullable=False, default=600)
    username = db.Column(db.String(30), nullable=False)
    public = db.Column(db.Boolean(), nullable=False, default=True)

    def __repr__(self):
        return "<ID: {}, Name: {}, Username: {}, Public: {}".format(
            self.loc_id,self.name,self.username,self.public)

#Disclaimer: I make no claims on the security of this app
class Users(db.Model):
    username = db.Column(db.String(30), unique=True, nullable=False, primary_key=True)
    passhash = db.Column(db.Unicode(), nullable=False)
    
    def __repr__(self):
        return "<Username: {}>".format(self.username)

class ColorSchemes(db.Model):
    col_id = db.Column(db.Integer(), unique = True, nullable = False, primary_key = True, autoincrement = True)
    username = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(30), nullable=False, default="Untitled")
    public = db.Column(db.Boolean(), nullable=False, default=True)
    col_state = db.Column(db.Text(), default = "")
    

@app.route("/",methods=["GET","POST"])
def home():
    is_logged_in = "user" in session
    if is_logged_in:
        username=session["user"]
    else:
        username=None

    """if is_logged_in and request.form:
        data=request.form
        is_public=True if data.get("private") is None else False
        location=Locations(name=data.get("name"),
                           x=data.get("x"),
                           y=data.get("y"),
                           zoom=data.get("zoom"),
                           limit=data.get("limit"),
                           public=is_public,
                           username=session["user"])
        db.session.add(location)
        db.session.commit()
        session["loc_id"]=location.loc_id
        thumbnail = open(os.path.join(app.config["thumbnails"],
                                      str(location.loc_id)), "w")
        thumbnail.write(data.get("preview"))
        thumbnail.close()
    """
    if "loc_id" in session:
        loc_id=session["loc_id"]
        location=Locations.query.filter_by(loc_id=loc_id).first()
        if not (location is None):
            if location.public==False and location.username!=username:
                location=None
        if location is None:
            location=Locations
            xcor=0
            ycor=0
            zoom=1
            limit=600
            loc_name="Untitled"
        else:
            xcor=location.x
            ycor=location.y
            zoom=location.zoom
            limit=location.limit
            loc_name=location.name
    else:
        xcor=0
        ycor=0
        zoom=1
        limit=600
        loc_name="Untitled"
    if "col_id" in session:
        col_id=session["col_id"]
        print(col_id)
        color_scheme=ColorSchemes.query.filter_by(col_id=col_id).first()
        if not (color_scheme is None):
            if color_scheme.public==False and color_scheme.username!=username:
                colorScheme=None
        if color_scheme is None:
            col_state=""
            col_name="Untitled"
        else:
            col_state=str(color_scheme.col_state)
            col_name=color_scheme.name
    else:
        col_state=""
        col_name="Untitled"
    selectColTemp=selectCol()
    
    selectLocTemp=selectLoc()

    return render_template("index.html",
                           loc_name=loc_name,
                           x=xcor,
                           y=ycor,
                           zoom=zoom,
                           limit=limit,
                           col_name=col_name,
                           col_state=col_state,
                           is_logged_in=is_logged_in,
                           username=username,
                           selectCol=selectColTemp,
                           selectLoc=selectLocTemp)

def get_preview(loc_id):
    filename = os.path.join(app.config["thumbnails"],
                            secure_filename(str(loc_id)))
    if(os.path.exists(filename)):
        file = open(filename, "r")
        uri = file.readline()
        file.close()
        return uri


@app.route("/saveLoc", methods=["POST"])
def saveLoc():
    is_logged_in = "user" in session
    if is_logged_in:
        username=session["user"]
    else:
        username=None

    if is_logged_in and request.form:
        data=request.form
        is_public=True if data.get("private") is None else False
        location=Locations(name=data.get("name"),
                           x=data.get("x"),
                           y=data.get("y"),
                           zoom=data.get("zoom"),
                           limit=data.get("limit"),
                           public=is_public,
                           username=session["user"])
        db.session.add(location)
        db.session.commit()
        session["loc_id"]=location.loc_id
        thumbnail = open(os.path.join(app.config["thumbnails"],
                                      str(location.loc_id)), "w")
        thumbnail.write(data.get("preview"))
        thumbnail.close()
    return redirect("/")

@app.route("/saveCol", methods=["POST"])
def saveCol():
    is_logged_in = "user" in session
    if is_logged_in:
        username=session["user"]
    else:
        username=None

    if is_logged_in and request.form:
        data=request.form
        is_public=True if data.get("private") is None else False
        color_scheme = ColorSchemes(col_state = data.get("col_state"),
            name=data.get("name"),
            username=username,
            public=is_public)
        db.session.add(color_scheme)
        db.session.commit()
        session["col_id"]=color_scheme.col_id
        """thumbnail = open(os.path.join(app.config["thumbnails"],
                                      str(location.loc_id)), "w")
        thumbnail.write(data.get("preview"))
        thumbnail.close()"""
    return redirect("/")


#@app.route("/selectLoc",methods=["GET","POST"])
def selectLoc():
    is_logged_in = "user" in session
    if is_logged_in:
        username=session["user"]
    else:
        username=None
    
    public_locations=Locations.query.filter(Locations.public==True,Locations.username!=username).all()
    if is_logged_in:
        user_locations=Locations.query.filter_by(username=session["user"]).all()
    else:
        user_locations=[]
    if request.form:
        session["loc_id"]=request.form.get("loc_id")
        return redirect("/")
    return render_template("selectLoc.html",
                           public_locations=public_locations,
                           user_locations=user_locations,
                           is_logged_in=is_logged_in,
                           username=username,
                           get_preview=get_preview)

#@app.route("/selectCol", methods=["GET","POST"])
def selectCol():
    is_logged_in = "user" in session
    if is_logged_in:
        username=session["user"]
    else:
        username=None
    
    public_colors=ColorSchemes.query.filter(ColorSchemes.public==True,ColorSchemes.username!=username).all()
    if is_logged_in:
        user_colors=ColorSchemes.query.filter_by(username=session["user"]).all()
    else:
        user_colors=[]
    if request.form:
        session["col_id"]=request.form.get("col_id")
        return redirect("/")
    return render_template("selectCol.html",
                           public_color_schemes=public_colors,
                           user_colors=user_colors,
                           is_logged_in=is_logged_in,
                           username=username)

@app.route("/locations",methods=["GET","POST"])
def locations():
    is_logged_in = "user" in session
    if is_logged_in:
        username=session["user"]
    else:
        username=None
    
    public_locations=Locations.query.filter(Locations.public==True,Locations.username!=username).all()
    if is_logged_in:
        user_locations=Locations.query.filter_by(username=session["user"]).all()
    else:
        user_locations=[]
    if request.form:
        session["loc_id"]=request.form.get("loc_id")
        return redirect("/")
    return render_template("locations.html",
                           public_locations=public_locations,
                           user_locations=user_locations,
                           is_logged_in=is_logged_in,
                           username=username,
                           get_preview=get_preview)

@app.route("/colorSchemes",methods=["GET","POST"])
def colorSchemes():
    is_logged_in = "user" in session
    if is_logged_in:
        username=session["user"]
    else:
        username=None
    
    public_colors=ColorSchemes.query.filter(ColorSchemes.public==True,ColorSchemes.username!=username).all()
    if is_logged_in:
        user_colors=ColorSchemes.query.filter_by(username=session["user"]).all()
    else:
        user_colors=[]
    if request.form:
        session["col_id"]=request.form.get("col_id")
        return redirect("/")
    return render_template("colorSchemes.html",
                           public_color_schemes=public_colors,
                           user_colors=user_colors,
                           is_logged_in=is_logged_in,
                           username=username)

@app.route("/delete",methods=["GET","POST"])
def delete():
    is_logged_in = "user" in session
    if is_logged_in:
        username=session["user"]
    else:
        return redirect("/select")
    if request.form:
        loc_id=request.form.get("loc_id")
        location=Locations.query.filter_by(loc_id=loc_id).first()
        if not (location is None):
            if location.username==username:
                db.session.delete(location)
                db.session.commit()
    return redirect("/selectCol")


@app.route("/login",methods=["GET","POST"])
def login():
    error_status=0
    if request.form:
        username=request.form.get("username")
        password=request.form.get("password")
        passhash=sha256_crypt.encrypt(password)
        user=Users.query.filter_by(username=username).first()
        if user is None:
            error_status=1
        elif not sha256_crypt.verify(password,user.passhash):
            error_status=1
        else:
            session["user"]=username
            return redirect("/")
    return render_template("login.html",error_status=error_status)


@app.route("/logout")
def logout():
    if "user" in session:
        if "user" in session: del session["user"]
        if "loc_id" in session: del session["loc_id"]
    return redirect("/")


@app.route("/register",methods=["GET","POST"])
def register():
    error_status=0
    if request.form:
        username=request.form.get("username")
        password=request.form.get("password")
        password2=request.form.get("password2")
        for c in username:
            if not (c.isalnum() or c in "`~!@#$%^&*()_-+={}|[]:;<>?"):
                error_status=1
                break
        else:
            if not Users.query.filter_by(username=username).first() is None:
                error_status=4
            elif len(password)<8:
                error_status=2
            elif password!=password2:
                error_status=3
        
        if error_status==0:
            passhash=sha256_crypt.encrypt(password)
            user=Users(username=username,passhash=passhash)
            db.session.add(user)
            db.session.commit()
            session["user"]=username
            return redirect("/")
    return render_template("register.html",error_status=error_status)

@app.route("/instructions")
def instructions():
    return render_template("instructions.html")


@app.route("/about")
def about():
    return render_template("about.html")


if __name__=="__main__":
    app.run(debug=True)
