import re
from flask_wtf import FlaskForm,Form
from wtforms import StringField,SelectField
from wtforms import validators
from wtforms.fields.core import BooleanField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, Length, ValidationError
from blog.models import User,Urun

class Register(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=6,max=25,message='username minimum 6 maximum 25 karakter olabilir')])
    password = PasswordField('Password',validators=[DataRequired(),validators.EqualTo('confirm',message='Şifreler eşleşmiyor')])
    email = StringField('Email',validators=[DataRequired()])
    is_admin = BooleanField('Kullanıcıaya Adminlik yetkisi verilsin mi ?')
    confirm = PasswordField('Repeat Password',validators=[DataRequired()])

    def validate_username(form,field):

        if  User.query.filter_by(username=form.username.data).first():
            raise ValidationError('Bu kullanıcı adı zaten kullanımda')

    def validate_email(form,field):
        email = form.email.data
        metin = email.split()
        if User.query.filter_by(email=email).first():
            raise ValidationError('Bu email zaten kullanımda')
      
        for i in metin:
           sonuc = re.search("(@gmail.com|.com.tr|@hotmail.com|@outlook.com|.edu)$",i)
           if sonuc:
             mail = sonuc.string
           else:
              raise ValidationError('Bu email kullanıma aykırıdır')
    def validate_password(form,field):
        password = form.password.data
        if len(password) < 8:
             raise ValidationError('Sifre 8 karakterden küçük olamaz')
        if  password.islower() == False and password.isupper() == False:
            veri = password.split()
            for a in veri:
                sonuc =  re.search("[A-Za-z0-9]+[A-Za-z0-9_+-.,][-*+.,?]",a)
                if sonuc:
                    print(sonuc.string)
        else:
            raise ValidationError('Şifreniz de en az bir rakam bir karakterden oluşmalıdır')
           
            


class Urun_form(FlaskForm):
    urun_kod = StringField('Urun_kimligi',validators=[DataRequired(),Length(min=6,max=12,message='ürün kodu minimum 6  maximum 12 karakter olabilir')])

    def validate_urun_kod(form,field):
        urun_kimlik = form.urun_kod.data.strip()
        print(urun_kimlik)
        if Urun.query.filter_by(urun_kodu=urun_kimlik).first():
            raise ValidationError("Bu Ürün koduna ait bir sipariş mevcut")


    
    
            

