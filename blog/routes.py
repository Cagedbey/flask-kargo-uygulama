from functools import reduce
from re import escape
import flask
from flask.helpers import url_for
from flask_login.utils import login_required
from blog.models import Status, User,Urun
from flask.templating import render_template
from blog import app,db
from flask import Blueprint, json,request,jsonify,redirect,flash
from flask_login import current_user, logout_user,login_user
from blog.forms import *

admin = Blueprint('admin',__name__,static_folder="static/assets/admin/panel/",template_folder="templates/admin/dist/")



@admin.route('/')
def index():
    if current_user.is_authenticated == True:
        urun = Urun.query.all()
        return render_template('index2.html',urun = urun,str=str,admin=current_user)
    else:
        return redirect(url_for('admin.login'))


@admin.route('/logout')
def logout():
    if current_user.is_authenticated == True:
        logout_user()
        return redirect(url_for('admin.login'))
    else:
        return redirect(url_for('admin.index'))



@admin.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated == True:
        return redirect(url_for('admin.index'))
    if request.method == "POST":
        username = request.form.get('username')
        psw = request.form.get('password')
        user = User.query.filter_by(username=username).first() or User.query.filter_by(email=username).first()
        if user and user.password == psw:
            login_user(user)
            return redirect(url_for('admin.index'))
        else: 
            flash('Hatalı kullanıcı adı veya şifre','danger')
            return redirect(url_for('admin.login'))
    
    return render_template('login.html')

@admin.route('/kayit',methods=['GET','POST'])
def register():
    form = Register()
    #if User.query.count():
        #return redirect(url_for('admin.login'))
    if request.method == "POST":
        if form.validate_on_submit():
                user = User(name = form.username.data,
                email = form.email.data,
                password = form.password.data,
                admin = form.is_admin.data)
                db.session.add(user)
                db.session.commit()
                logout_user()
                flash('tebrikler kaydınız oluşturulmuştur','success')
                return  redirect(url_for('admin.login'))
        else:
                message = form.errors
                flash(message,'warning')
                return  redirect(url_for('admin.register'))

    return render_template('register.html',form=form)

@admin.route('/create',methods=['GET','POST'])
@login_required
def create():
    form = Urun_form()
    urun_all = Status.query.all()
    if current_user.is_authenticated and current_user.is_admin == True:
       if request.method == "POST":
          if form.validate_on_submit():
            urun = form.urun_kod.data
            ekle = Urun(user=current_user,status=request.form.get('category'),urun=urun)
            db.session.add(ekle)
            db.session.commit()
            return redirect(url_for('admin.index'))
          else:
            message = form.errors
            flash(message,'warning')
            return  redirect(url_for('admin.create'))  
       return render_template('create.html',form=form,status = urun_all,admin=current_user)

    return redirect(url_for('admin.index'))
@admin.route('/status_add',methods=['GET','POST'])
@login_required
def status_add():
    if current_user.is_authenticated and current_user.is_admin == True:
       if request.method == "POST":
            gelen_veri = request.form.get('status_add',False)
            st = Status(status_name=gelen_veri)
            db.session.add(st)
            db.session.commit()
            return redirect(url_for('admin.status_add'))
       else:
           return render_template('category_add.html',durum=Status.query.all(),admin=current_user)

    return redirect(url_for('admin.index'))
       
    
@admin.route('/status_update/<id>',methods=['GET','POST'])
@login_required
def status_update(id):
    durum = Status.query.get_or_404(id)
    if current_user.is_authenticated and current_user.is_admin == True:
        if request.method == "POST":
            durum = Status.query.get_or_404(id)
            durum.status_name = request.form.get('status_update')
            db.session.commit()
            return redirect(url_for('admin.status_add'))
        else:
            return render_template('status_update.html',durum=durum,admin=current_user)
    return redirect(url_for('admin.index'))
    

@admin.route('/status_delete/<id>',methods=['GET','POST'])
@login_required
def status_delete(id):
  if current_user.is_authenticated and current_user.is_admin == True:
        durum = Status.query.get_or_404(id)
        db.session.delete(durum)
        db.session.commit()
        return redirect(url_for('admin.status_add'))
  return redirect(url_for('admin.index'))

@admin.route('/create_update/<id>',methods=['GET','POST'])
@login_required
def create_update(id):
    form = Urun_form()
    print(request.url.split('create_update')[1].replace('/',''))
    status = Status.query.all()
    durum = Urun.query.get_or_404(id)
    if current_user.is_authenticated and current_user.is_admin == True:
        if request.method == "POST":
            urun = Urun.query.get_or_404(id)
            urun.urun_kodu = form.urun_kod.data
            urun.status_id = request.form.get('category')
            db.session.commit()
            return redirect(url_for('admin.create_update',id=urun.id))
        else:
            return render_template('create_update.html',urun=durum,form=form,status=status,admin=current_user,request=request)
    else:
        return redirect(url_for('admin.index'))
@admin.route('/create_delete/<id>',methods=['GET','POST'])
@login_required
def create_delete(id):
   if current_user.is_authenticated and current_user.is_admin == True:
        urun = Urun.query.get_or_404(id)
        db.session.delete(urun)
        db.session.commit()
        return redirect(url_for('admin.index',id=urun.id))
   else:
       return redirect(url_for('admin.index'))
   
   

@app.errorhandler(401)
def unauthorized(e):
    return redirect(url_for('admin.index'))
@app.errorhandler(404)
def notfound(e):
    return redirect(url_for('admin.index'))
