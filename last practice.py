from datetime import datetime
import sqlite3
cnt = sqlite3.connect('e:/ftest.db')
islogin=False
isadmin=False
userid=""
########################################## create user table
# cnt.execute(''' CREATE TABLE users
# (ID INTEGER PRIMARY KEY,
#  fname CHAR(20),
#  lname CHAR(20),
#  addr CHAR(50),
#  grade INT(10),
#  username CHAR(15),
#  password CHAR(15),
#  edate CHAR(10),
#  ncode CHAR(15),
#  reserve1 CHAR(10))''')
# print('done')
# cnt.close()

############################################ create product table

# cnt.execute(''' CREATE TABLE products
# (ID INTEGER PRIMARY KEY,
#   pname CHAR(20),
#   quantity INT(30),
#   bprice INT(20),
#   sprice INT(20),
#   edate CHAR(15),
#   brand CHAR(40),
#   reserve1 CHAR(20))''')
# print('done')
# cnt.close()

######################################### create transactions table

# =============================================================================
# cnt.execute(''' CREATE TABLE transactios
# (ID INTEGER PRIMARY KEY,
#   uid INT(15),
#   pid INT(15),
#   bdate CHAR(15),
#   qnt INT(5),
#   comment CHAR(50),
#   reserve CHAR(30))''')
# print('done')
# cnt.close()
# 
# =============================================================================
############################################ main program
def validation(fname,lname,addr,username,password,cpassword,ncode):
    global cnt
    errorlist=[]
    if(fname=="" or lname=="" or addr=="" or username=="" or password=="" or cpassword=="" or ncode==""):
        msg='please fill all of blanks'
        errorlist.append(msg)
    if(len(password)<8):
        msg='pass lenght must be at least 8'
        errorlist.append(msg)
    if(password!=cpassword):
        msg='pass and confirm missmatch'
        errorlist.append(msg)
        
    if(not(ncode.isnumeric())):
        msg='national code should be numeric'
        errorlist.append(msg)
    
    sql='SELECT * FROM users WHERE username=? '
    cursor=cnt.execute(sql,(username,))
    rows=cursor.fetchall()
    if(len(rows)!=0):
        msg='username already exist'
        errorlist.append(msg)
        
    return errorlist


def submit():
    
    fname=input('please enter your name:  ')
    lname=input('please enter your last name:  ')
    addr=input('please enter your address:  ')
    grade=0
    edate=datetime.today().strftime('%y-%m-%d')
    username=input('please enter your username:  ')
    password=input('please enter your password:  ')
    cpassword=input('please enter your password confirmation:  ')
    ncode=input('please enter your national code:  ')
    result=validation(fname,lname,addr,username,password,cpassword,ncode)
    if(len(result)!=0):
        for err_msg in result:
            print(err_msg)
        return
    sql=''' INSERT INTO users(fname,lname,addr,grade,username,password,edate,ncode)
    VALUES(?,?,?,?,?,?,?,?)'''
    cnt.execute(sql,(fname,lname,addr,grade,username,password,edate,ncode))
    cnt.commit()
    print('submit done successfully')
    
    

def login():
    global islogin,isadmin,userid
    if(islogin):
        print('you are already logged in')
        return
    user=input('please enter username:  ')
    passw=input('please enter password:  ')
    sql=''' SELECT username,id FROM users WHERE  (username=? AND password=?)'''
    cursor=cnt.execute(sql,(user,passw))
    row=cursor.fetchone()
    if(not(row)):
        print('wrong user or pass')
        return
    print('welcome to your account')
    userid=row[1]
        
    islogin=True
    if user=='admin':
        isadmin=True
    
def logout():
    global islogin,isadmin,userid
    islogin=False
    isadmin=False
    userid=""
    print('you are logged out now')
    
def mproducts():
    global islogin,isadmin
    if(islogin==False or isadmin==False):
        print('you are not allowed for this action')
        return
    
    Products_name=input('please enter product name:  ')
    quantity=input('please enter quantity  ')
    buy_price=input('please enter buy price:  ')
    sell_price=input('please enter buy sell price:  ')
    ex_date=""
    brand=input('please enter brand name:  ')
    ###############
    sql="SELECT pname FROM products WHERE pname=? "
    cursor=cnt.execute(sql,(Products_name,))
    rows=cursor.fetchall()
    if(len(rows)>0):
        print('product name already exist')
        return
    ###############
    sql=''' INSERT INTO products(pname,stock,bprice,sprice,exdate,brand)
    VALUES(?,?,?,?,?,?)'''
    cnt.execute(sql,(Products_name,quantity,buy_price,sell_price,ex_date,brand))
    cnt.commit()
    print('data inserted successfully')
    
def buy():
    global islogin,userid
    if(islogin==False):
        print('first you must login')
        return
    bdate=datetime.today().strftime('%y-%m-%d')
    pname=input('enter a product name you want to buy:  ')
    sql="SELECT * FROM products WHERE pname=?"
    cursor=cnt.execute(sql,(pname,))
    row=cursor.fetchone()
    if(not(row)): #natune chizio bargardune false ro barmigardune
        print('wrong product name')
        return
    print('product:',row[1],'Q:',row[2],' brand:',row[6],' price:',row[4])
    num=int(input('number of products? '))
    if(num<=0):
        print('wrong number')
        return
    if(num>int(row[2])):
        print('not enough number of products')
        return
    print('total cost ',num*row[4])
    confirm=input('are you sure? yes/no')
    if(confirm!='yes'):
        print('canceled by user')
        return
    newquant=int(row[2])-num
    sql="UPDATE products SET stock=? WHERE pname=?"
    cnt.execute(sql,(newquant,pname))
    print('thanks for your shopping')
    cnt.commit()
    
    sql='''INSERT INTO transactios (uid,pid,bdate,qnt)
           VALUES(?,?,?,?)'''
    cnt.execute(sql,(userid,row[0],bdate,num))
    cnt.commit()
    
    
    
    
    
    
def plist():
    sql=" SELECT pname,quantity FROM products WHERE quantity>0 "
    cursor=cnt.execute(sql)
    rows=cursor.fetchall()
    for row in rows:
        print(row[0],' Q:',row[1])
        
        
        
def alltrc():
    global isadmin
    if not(isadmin):
        print("you need to login first")
        return
    sql='''SELECT users.lname,transactios.bdate,products.pname,transactios.qnt from transactios inner join users
    on transactios.uid=users.id
    inner join products
    on transactios.pid=products.id
    '''
    cursor=cnt.execute(sql)
    for row in cursor:
        print('user: ' ,row[0],"date: ",row[1],"products :", row[2],'qnt: ',row[3])
        
        
        

while(True):
    plan=input('please enter your plan:  ')
    if(plan=='submit'):
        submit()
    elif(plan=='login'):
        login()
    elif(plan=='logout'):
        logout()
    elif(plan=='manage products'):
        mproducts()
    elif(plan=='buy'):
        buy()
    elif(plan=='plist'):
        plist()
    elif(plan=='exit'):
        break
    elif(plan=="all trans"):
        alltrc()
    else:
        print('wrong input')