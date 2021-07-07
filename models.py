from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy.sql.expression import false, true
from sqlalchemy.sql.schema import ForeignKey

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuario'

    id= db.Column(db.Integer, primary_key=True)

    nombre = db.Column(db.String(50), nullable=False) 
    apellido = db.Column(db.String(50), nullable=False) 
    correo = db.Column(db.String(50), nullable=False) 
    contrasenna = db.Column(db.String(50), nullable=False) 
    pais = db.Column(db.Integer, foreing_key = True, nullable=False)
    fecha_registro =  db.Column(db.DateTime(), nullable=False, default=db.func.current_timestamp())


    @classmethod
    def create(cls,id,nombre,apellido,correo,contrasenna,pais,fecha_registro):
        usuario = Usuario(id=id,nombre=nombre,apellido=apellido, correo=correo, contrasenna=contrasenna,pais=pais,fecha_registro=fecha_registro)
        return usuario.save()
    
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except:
            return False

    def json(self):
        return{
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'correo': self.correo,
            'contrasenna': self.contrasenna,
            'pais': self.pais,
            'fecha_registro': self.fecha_registro
        }       

    def update(self):
        self.save()
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()

            return True
        except:
            return False


class Pais(db.Model):
    __tablename__ = 'pais'
    cod_pais = db.Column(db.Integer, primary_key=True)
    nombre= db.Column(db.String(45), nullable=False) 

    @classmethod
    def create(cls, cod_pais, nombre):
        pais = Pais(cod_pais=cod_pais,nombre=nombre)
        return pais.save()

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except:
            return False

    def json(self):
        return{
            'cod_pais': self.cod_pais,
            'nombre': self.nombre
        }

    def update(self):
        self.save()
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()

            return True
        except:
            return False


class Cuenta_Bancaria(db.Model):
    __tablename__='cuenta_bancaria'
    numero_cuenta = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, foreing_key=True)
    balance = db.Column(db.Float, nullable=False)

    @classmethod
    def create(cls, numero_cuenta, id_usuario, balance):
        cuenta_bancaria =Cuenta_Bancaria(numero_cuenta=numero_cuenta, id_usuario=id_usuario, balance=balance)
        return cuenta_bancaria.save()

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except:
            return False

    def json(self):
        return{
            'numero_cuenta': self.numero_cuenta,
            'id_usuario': self.id_usuario,
            'balance': self.balance
        }

    def update(self):
        self.save()
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()

            return True
        except:
            return False   


class Usuario_Tiene_Moneda(db.Model):
    __tablename__='usuario_tiene_moneda'
    id_moneda = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, foreing_key=True)
    balance = db.Column(db.Float, nullable=False)

    @classmethod
    def create(cls, id_moneda, id_usuario, balance):
        usuario_tiene_moneda =Usuario_Tiene_Moneda(id_moneda=id_moneda, id_usuario=id_usuario, balance=balance)
        return usuario_tiene_moneda.save()

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except:
            return False
    
    def json(self):
        return{
            'id_moneda': self.id_moneda,
            'id_usuario': self.id_usuario,
            'balance': self.balance
        }

    def update(self):
        self.save()
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()

            return True
        except:
            return False


class Moneda(db.Model):
	__tablename__ = 'moneda'
	id = db.Column(db.Integer, primary_key=True)
	nombre = db.Column(db.String(80), nullable=False) 
	sigla = db.Column(db.String(10), nullable=False)
	
	@classmethod
	def create(cls, id, nombre, sigla):
		moneda = Moneda(id=id, nombre=nombre, sigla = sigla)
		return moneda.save()

	def save(self):
		try:
			db.session.add(self)
			db.session.commit()

			return self
		except:
			return False
	def json(self):
		return {
			'id': self.id,
			'nombre': self.nombre,
			'sigla': self.sigla
		}
	def update(self):
		self.save()
	def delete(self):
		try:
			db.session.delete(self)
			db.session.commit()

			return True
		except:
			return False


class Precio_Moneda(db.Model):
    __tablename__ = 'precio_moneda'
    fecha = db.Column(db.DateTime, primary_key=True , default=db.func.current_timestamp())
    valor = db.Column(db.Float,nullable=False)
    id_moneda = db.Column(db.Integer, nullable=False)
	
	
    @classmethod
    def create(cls, fecha, valor, id_moneda):
        precio= Precio_Moneda(fecha=fecha ,valor=valor,id_moneda=id_moneda)
        return precio.save()
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except:
            return False
    def json(self):
        return {
            'fecha': self.fecha,
            'valor': self.valor,
            'id_moneda':self.id_moneda			
        }
    def update(self):
        self.save()
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit() 
            return True
        except:
            return False


