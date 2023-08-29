from flask import *
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine,text
import random
#from PIL import Image
import base64
import smtplib
from io import BytesIO
from PIL import Image
from jinja2 import Environment
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from datetime import datetime





local_server= True
app=Flask(__name__)
app.secret_key="cns"

app.config['SQLALCHEMY_DATABASE_URI']='Nikhilgowda13.mysql.pythonanywhere-services.com/Nikhilgowda13$student_view'
#engine = create_engine('mysql+pymysql://root:@localhost/studentview')
db=SQLAlchemy(app)

class Products(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, primary_key=True)
    usn=db.Column(db.String(100), nullable=False)
    studentname=db.Column(db.String(100), nullable=False)
    email=db.Column(db.String(100), nullable=False)

class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    filename = db.Column(db.String(100), nullable=False)
    image_data=db.Column(db.LargeBinary)
    product_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, primary_key=True)
    usn=db.Column(db.String(100), nullable=False)
    student_name=db.Column(db.String(100), nullable=False)

class Subimages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    filename = db.Column(db.String(100), nullable=False)
    image_data=db.Column(db.LargeBinary)   

class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    club = db.Column(db.String(100), primary_key=True)
    descp =db.Column(db.String(1000), nullable=False)

class Chatroom(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    message = db.Column(db.String(1000), nullable=False)
    #timestamp=db.Column(db.Timestamp(6),nullable=False)

class Alumni(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100), nullable=False)
    image_data=db.Column(db.LargeBinary)
    yob=db.Column(db.String(4), nullable=False)
    link=db.Column(db.String(4), nullable=False)
    email=db.Column(db.String(4), nullable=False)
    position=db.Column(db.String(100), nullable=False)

@app.route("/",methods=['GET', 'POST'])
def home():
    return render_template('home.html')



@app.route("/sell",methods=['GET', 'POST'])
def sell():
     if request.method=='POST':
         name=request.form.get('name')
         price=request.form.get('price')
         images = request.files.getlist('images[]')
         sname=request.form.get('studentname')
         usn=request.form.get('usn')
         id=random.randint(0,10000000)
         semail=request.form.get('email')
         #create new product
         product = Products(id=id,name=name, price=price,usn=usn,studentname=sname,email=semail)
         #product = products(name=name, price=price,usn=usn,studentname=sname)
         image=images[0]

         db.session.add(product)
         db.session.commit()
         
         filename=image.filename
         image_data = BytesIO(image.read())
         img=Images(product_id=id, filename=filename,image_data=image_data.getvalue(),product_name=name, price=price,usn=usn,student_name=sname)
         print("working")
         db.session.add(img)
         db.session.commit()
         
         subimages = request.files.getlist('images[]')
         print(Products.id)
         # save the images to the database
         for image in subimages[1:]:
             filename=image.filename
             image_data = BytesIO(image.read())
             print(filename)
             img=Subimages(product_id=id, filename=filename,image_data=image_data.getvalue())
             db.session.add(img)
             db.session.commit()

     
     return render_template('sell.html')





@app.route("/buy",methods=['GET', 'POST'])
def buy():
    product=Products.query.all()
    images = Images.query.all()
    imglist=[]
    


    count=0
    for test_img in images:
        count+=1
        print(test_img.product_id)
        img_data =test_img.image_data
        img_data=base64.b64encode(img_data).decode('utf-8')
        #print(type(img_data))
        #print("test_img*************",test_img.id)
        imglist.append(img_data)
    print( "count od=f images ", count) 
    return render_template('buy.html', img_list=imglist,products=images)
        #return "true"
    
    
    
    # return "True"
    # img_list = []
    
    
    # for image in images:
    #     img_data = BytesIO(image.image_data)
    #     img = Image.open(img_data)
        
    #     img_base64 = base64.b64encode(img.tobytes()).decode('utf-8')
    #     # print("****************",img_base64)
    #     img_list.append(img_base64)
    #     # print("*************",img_list)

@app.route("/buy_confirmation/<int:id>",methods=['GET', 'POST'])
def buy_confirmation(id):
    #query_text = "SELECT * FROM `subimages` WHERE product_id=7778588"
    #query=text(query_text)
    #subimage = engine.execute(query)
    product=Products.query.filter_by(id=id).first()
    print(id)
    image=Images.query.filter_by(product_id=id).first()
    if image:
        print("image present ",image.product_id)
    test_img=image
    img_data =test_img.image_data
    img_data=base64.b64encode(img_data).decode('utf-8')
    imglist=[]
    subimage=db.engine.execute(f"SELECT * FROM `subimages` WHERE product_id='{id}'")
    print(type(subimage))
    count=0
    for test_img in subimage:
        count+=1
        print(test_img.product_id)
        img_data =test_img.image_data
        img_data=base64.b64encode(img_data).decode('utf-8')
        #print(type(img_data))
        #print("test_img*************",test_img.id)
        imglist.append(img_data)



    if request.method=="POST":
        name=request.form.get('studentname')
        usn=request.form.get('name')
        sem=request.form.get('sem')
        branch=request.form.get('branch')
        
        print(name,branch,sem)
        # Define the email addresses and message
        sender_email = "Gecarcade@gmail.com"
        receiver_email = 'nikhilgowda13121@gmail.com'
        password = 'sikohjpzwslajsul'

        message = MIMEMultipart()
        message["Subject"] = "Example subject line"
        message["From"] = sender_email
        message["To"] = receiver_email

        print(product.name)
        text = 'ur product '+product.name+' have a buy request from '+name+' of '+sem+'th sem of '+branch+' branch'
        html = """\
        <html>
        <body>
            <p>This is an example email message.</p>
            <img src="cid:image1">
        </body>
        </html>
        """
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)

        # Send the email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())


        return render_template('orderplaced.html')

    return render_template("buy_confirmation.html",product=product,image=img_data,img_list=imglist)








        
        
        #receiver_mailid=product.email
        #server=smtplib.SMTP('smtp@gmail.com',587)
        #server.startls()
        #server.login('Gecarcade@gmail.com','gech_016')
        #server.sendmail('Gecarcade@gmail.com',product.email,'ur product'+product.name+'have a buy request from'+name+'of '+sem+'th sem of'+branch+'branch')
        #print('mailsent')



       
    

#password='sikohjpzwslajsul'





@app.route("/sgpa",methods=['GET', 'POST'])
def sgpa():
    def grade(marks):
        if marks>=90 and marks<=100:
            return(10)
        elif marks>=80 and marks<90:
            return(9)
        elif marks>=70 and marks<80:
            return(8)
        elif marks>=60 and marks<70:
            return(7)
        elif marks>=50 and marks<60:
            return(6)
        elif marks>=45 and marks<50:
            return(5)
        elif marks>=40 and marks<45:
            return(4)
        else:
            return (0)
    if request.method=='POST':
        sub1=float(request.form.get('sub1'))
        sub1=grade(sub1)*4
        sub2=float(request.form.get('sub2'))
        sub2=grade(sub2)*4
        sub3=float(request.form.get('sub3'))
        sub3=grade(sub3)*4
        sub4=float(request.form.get('sub4'))
        sub4=grade(sub4)*3
        sub5=float(request.form.get('sub5'))
        sub5=grade(sub5)*3
        sub6=float(request.form.get('sub6'))
        sub6=grade(sub6)*3
        sub7=float(request.form.get('sub7'))
        sub7=grade(sub7)*2
        sub8=float(request.form.get('sub8'))
        sub8=grade(sub8)*2
        
        total=(sub1+sub2+sub3+sub4+sub5+sub6+sub7+sub8)
        sgpa =total/25
        percentage=(sgpa-0.75)*10
        return render_template('sgparesult.html',sgpa=sgpa,percentage=percentage)

    return render_template('sgpa.html',sgpa=0)


@app.route("/cgpa",methods=['GET', 'POST'])
def cgpa():
    if request.method=='POST':
        count=0
        sem1=float(request.form.get('sem1'))
        if sem1>0:
            count+=1
        sem2=float(request.form.get('sem2'))
        if sem2>0:
            count+=1
        sem3=float(request.form.get('sem3'))
        if sem3>0:
            count+=1
        sem4=float(request.form.get('sem4'))
        if sem4>0:
            count+=1
        sem5=float(request.form.get('sem5'))
        if sem5>0:
            count+=1
        sem6=float(request.form.get('sem6'))
        if sem6>0:
            count+=1
        sem7=float(request.form.get('sem7'))
        if sem7>0:
            count+=1
        sem8=float(request.form.get('sem8'))
        if sem8>0:
            count+=1
        cgpa=(sem1*25+sem2*25+sem3*25+sem4*25+sem5*25+sem6*25+sem7*25+sem8*25)/(25*count)
        percentage=(cgpa-0.75)*10
        print(cgpa)
        return render_template('result.html',cgpa=cgpa,percentage=percentage)




    return render_template('cgpa.html')

@app.route("/events",methods=['GET', 'POST'])
def events():
    event = Events.query.all()
    #print(event[1].name)
    return render_template('events.html',event=event)

@app.route("/admin_verification",methods=['GET', 'POST'])
def admin_verification():
    if request.method=="POST":
        admin=['anjali@admin','nikhil@admin','temp_admin']
        pswd=['abc3']
        temp_pswd=['js123']
        name=request.form.get('name')
        password=request.form.get('Password')
        print(name,password)
        if name in admin:
            if name=='temp_admin' and password in temp_pswd:
                return render_template('addevents.html')
            elif (name=='anjali@admin' or name=='nikhil@admin') and ( password in pswd):
                return render_template('addevents.html')
            else:
                return render_template('loginfailed.html')
        else:
            return render_template('loginfailed.html')


    

    return render_template('admin_verification.html')



@app.route("/club",methods=['GET', 'POST'])
def club():
    return render_template('club.html')

@app.route("/developers",methods=['GET', 'POST'])
def developers():
    return render_template('developers.html')


@app.route("/addevents",methods=['GET', 'POST'])
def addevents():
    if request.method=='POST':
        
        name=request.form.get('name')
        club=request.form.get('club')
        descp=request.form.get('desc')
        event = Events(name=name, club=club,descp=descp)
         
        db.session.add(event)
        db.session.commit()


    return render_template('addevents.html')



    
    
    
    
    
    
    
@app.route("/chatroom",methods=['GET', 'POST'])
def chatroom():
    if request.method=='POST':
        message=request.form.get('message')
        timestamp = datetime.now()
        #print(type(timestamp))
        #print(timestamp)
        chat = Chatroom(message=message)
         #product = products(name=name, price=price,usn=usn,studentname=sname)
         

        db.session.add(chat)
        db.session.commit()
    messages=db.engine.execute(f"SELECT * FROM `chatroom` ORDER BY id ")
    count=0
    for i in messages:
        count+=1
    #print("message count",count)
    return render_template('chatroom.html',messages=messages)

@app.route("/alumni",methods=['GET', 'POST'])
def alumni():
    alumnis = Alumni.query.all()
    imglist=[]
    


    count=0
    for alumni in alumnis:
        count+=1
        #print(test_img.product_id)
        img_data =alumni.image_data
        img_data=base64.b64encode(img_data).decode('utf-8')
        #print(type(img_data))
        #print("test_img*************",test_img.id)
        imglist.append(img_data)
    # 
    
    return render_template('alumni.html', img_list=imglist,alumnis=alumnis)


@app.route("/admin_verification1",methods=['GET', 'POST'])
def admin_verification1():
    if request.method=="POST":
        admin=['anjali@admin','nikhil@admin','temp_admin']
        pswd=['abc3']
        temp_pswd=['js123']
        name=request.form.get('name')
        password=request.form.get('password')
        
        if name in admin:
            if name=='temp_admin' and password in temp_pswd:
                return render_template('addalumni.html')
            elif (name=='anjali@admin' or name=='nikhil@admin') and ( password in pswd):
                return render_template('addalumni.html')
            else:
                return render_template('loginfailed.html')
        else:
            return render_template('loginfailed.html')


    

    return render_template('admin_verification1.html')


@app.route("/addalumni",methods=['GET', 'POST'])
def addalumni():
    if request.method=='POST':
        
        name=request.form.get('name')
        yob=request.form.get('yob')
        position=request.form.get('position')
        images = request.files.getlist('images[]')
        email=request.form.get('email')
        link=request.form.get('link')
        
        image=images[0]

        
         
        filename=image.filename
        image_data = BytesIO(image.read())
        alumni=Alumni(name=name,yob=yob,position=position,image_data=image_data.getvalue(),link=link,email=email)
         
        db.session.add(alumni)
        db.session.commit()


    return render_template('addalumni.html')

if __name__=='__main__':
    app.config['UPLOAD_FOLDER'] = 'static/uploads/'
    app.run(debug=True)
