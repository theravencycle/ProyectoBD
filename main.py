from flask import Flask, json
from flask import jsonify
from config import config
from models import Pais, Usuario,Cuenta_Bancaria, Usuario_Tiene_Moneda , Moneda, Precio_Moneda ,db 
from flask import request
from sqlalchemy import extract, func


def create_app(enviroment):
	app = Flask(__name__)
	app.config.from_object(enviroment)
	with app.app_context():
		db.init_app(app)
		db.create_all()
	return app

enviroment = config['development']
app = create_app(enviroment)


@app.route('/api/v1/usuario', methods=['GET'])
def get_usuarios():
	usuarios = [ usuario.json() for usuario in Usuario.query.all() ] 
	return jsonify({'Usuarios': usuarios})

@app.route('/api/v1/usuario/<id>', methods=['GET'])
def get_usuario(id):
	usuario = Usuario.query.filter_by(id=id).first()
	if usuario is None:
		return jsonify({'message': 'El usuario no existe'}), 404
	return jsonify({'user': usuario.json() })

'''Al formar el Usuario.create aca es donde sale el error '''
@app.route('/api/v1/usuario/', methods=['POST'])
def create_usuario():
	json = request.get_json(force=True)
	if json.get('nombre') is None:
		return jsonify({'message': 'El formato está mal'}), 400
	user = Usuario.create(json['id'],json['nombre'],json['apellido'],json['correo'],json['contraseña'],json['pais'],json['fecha_registro'])
	return jsonify({'usuario': user.json() })

@app.route('/api/v1/usuario/<id>', methods=['PUT'])
def update_usuario(id):
	user = Usuario.query.filter_by(id=id).first()
	if user is None:
		return jsonify({'message': 'El usuario no existe'}), 404
	json = request.get_json(force=True)

	if json.get('nombre') is None or json.get('apellido') is None or json.get('correo') is None or json.get('contraseña') is None or json.get('pais') is None :
		return jsonify({'message': 'Solicitud Incorrecta'}), 400

	user.nombre = json['nombre']
    #user.apellido = json['apellido']  #Dezconozco porque al agregar los demas valores, me tiraba error 
    
	user.update()
	return jsonify({'usuario': user.json()})

@app.route('/api/v1/usuario/<id>', methods=['DELETE'])
def delete_usuario(id):
	user = Usuario.query.filter_by(id=id).first()
	if user is None:
		return jsonify({'message': 'El usuario no existe'}), 404
	user.delete()
	return jsonify({'usuario': user.json() })



@app.route('/api/v1/pais', methods=['GET'])
def get_paiss():
	paises = [ pais.json() for pais in Pais.query.all() ] 
	return jsonify({'Paises': paises})

@app.route('/api/v1/pais/<cod_pais>', methods=['GET'])
def get_pais(cod_pais):
	pais = Pais.query.filter_by(cod_pais=cod_pais).first()
	if pais is None:
		return jsonify({'message': 'El pais no existe'}), 404
	return jsonify({'pais': pais.json() })

@app.route('/api/v1/pais/', methods=['POST'])
def create_pais():
	json = request.get_json(force=True)
	if json.get('nombre') is None:
		return jsonify({'message': 'El formato está mal'}), 400
	pais = Pais.create(json['nombre'])
	return jsonify({'pais': pais.json() })

@app.route('/api/v1/pais/<cod_pais>', methods=['PUT'])
def update_pais(cod_pais):
	pais = Pais.query.filter_by(cod_pais=cod_pais).first()
	if pais is None:
		return jsonify({'message': 'El pais no existe'}), 404
	json = request.get_json(force=True)

	if json.get('nombre') is None or json.get('cod_pais') is None :
		return jsonify({'message': 'Solicitud Incorrecta'}), 400

	pais.nombre = json['nombre']
	pais.update()
	return jsonify({'pais': pais.json()})

@app.route('/api/v1/pais/<cod_pais>', methods=['DELETE'])
def delete_pais(cod_pais):
	pais = Pais.query.filter_by(cod_pais=cod_pais).first()
	if pais is None:
		return jsonify({'message': 'El Pais no existe'}), 404
	pais.delete()
	return jsonify({'usuario': pais.json() })



@app.route('/api/v1/cuenta_bancaria', methods=['GET'])
def get_cuenta_bancarias():
	cuentas = [ cuenta_bancaria.json() for cuenta_bancaria in Cuenta_Bancaria.query.all() ] 
	return jsonify({'cuenta_bancaria': cuentas})

@app.route('/api/v1/cuenta_bancaria/<numero_cuenta>', methods=['GET'])
def get_cuenta_bancaria(numero_cuenta):
	cuenta_bancaria = Cuenta_Bancaria.query.filter_by(numero_cuenta=numero_cuenta).first()
	if cuenta_bancaria is None:
		return jsonify({'message': 'La cuenta no existe'}), 404
	return jsonify({'cuenta_bancaria': cuenta_bancaria.json() })

@app.route('/api/v1/cuenta_bancaria/', methods=['POST'])
def create_cuenta_bancaria():
	json = request.get_json(force=True)
	if json.get('cuenta_bancaria') is None or json.get('id_usuario') is None or json.get('cuenta_bancaria') is None:
		return jsonify({'message': 'El formato está mal'}), 400
	cuenta_bancarria = Cuenta_Bancaria.create(json['numero_cuenta'],json['id_usuario'],json['balance'])
	return jsonify({'cuenta_bancaria': cuenta_bancarria.json() })

@app.route('/api/v1/cuenta_bancaria/<numero_cuenta>', methods=['PUT'])
def update_cuenta_bancaria(numero_cuenta):
	cuenta_bancaria = Cuenta_Bancaria.query.filter_by(numero_cuenta=numero_cuenta).first()
	if cuenta_bancaria is None:
		return jsonify({'message': 'La cuenta no existe'}), 404
	json = request.get_json(force=True)

	if json.get('numero_cuenta') is None or json.get('id_usuario') is None or json.get('balance') is None:
		return jsonify({'message': 'Solicitud Incorrecta'}), 400

	cuenta_bancaria.numero_cuenta = json['numero_cuenta']
	cuenta_bancaria.update()
	return jsonify({'cuenta_bancaria': cuenta_bancaria.json()})

@app.route('/api/v1/cuenta_bancaria/<numero_cuenta>', methods=['DELETE'])
def delete_cuenta_bancaria(numero_cuenta):
	cuenta_bancaria = Cuenta_Bancaria.query.filter_by(numero_cuenta=numero_cuenta).first()
	if cuenta_bancaria is None:
		return jsonify({'message': 'La cuenta no existe'}), 404
	cuenta_bancaria.delete()
	return jsonify({'cuenta_bancaria': cuenta_bancaria.json() })



@app.route('/api/v1/usuario_tiene_moneda', methods=['GET'])
def get_usuario_tiene_monedas():
	usuarios = [ usuario_tiene_moneda.json() for usuario_tiene_moneda in Usuario_Tiene_Moneda.query.all() ] 
	return jsonify({'usuario_tiene_moneda': usuarios})

@app.route('/api/v1/usuario_tiene_moneda/<id_usuario>', methods=['GET'])
def get_usuario_tiene_moneda(id_usuario):
	usuario_tiene_moneda = Usuario_Tiene_Moneda.query.filter_by(id_usuario=id_usuario).first()
	if usuario_tiene_moneda is None:
		return jsonify({'message': 'Las monedas del usuario no existen'}), 404
	return jsonify({'usuario_tiene_moneda': usuario_tiene_moneda.json() })

@app.route('/api/v1/usuario_tiene_moneda/', methods=['POST'])
def create_usuario_tiene_moneda():
	json = request.get_json(force=True)
	if json.get('id_moneda') is None or json.get('id_usuario') is None or json.get('balance') is None:
		return jsonify({'message': 'El formato está mal'}), 400
	usuario_tiene_moneda = Usuario_Tiene_Moneda.create(json['id_moneda'],json['id_usuario'],json['balance'])
	return jsonify({'usuario_tiene_moneda': usuario_tiene_moneda.json() })

@app.route('/api/v1/usuario_tiene_moneda/<id_usuario>', methods=['PUT'])
def update_usuario_tiene_moneda(id_usuario):
	usuario_tiene_moneda = Usuario_Tiene_Moneda.query.filter_by(id_usuario=id_usuario).first()
	if usuario_tiene_moneda is None:
		return jsonify({'message': 'La monedas no existen'}), 404
	json = request.get_json(force=True)

	if json.get('id_moneda') is None or json.get('id_usuario') is None or json.get('balance') is None:
		return jsonify({'message': 'Solicitud Incorrecta'}), 400

	usuario_tiene_moneda.id_moneda = json['id_moneda']
	usuario_tiene_moneda.update()
	return jsonify({'Usuario_Tiene_moneda': usuario_tiene_moneda.json()})

@app.route('/api/v1/usuario_tiene_moneda/<id_usuario>', methods=['DELETE'])
def delete_usuario_tiene_moneda(id_usuario):
	usuario_tiene_moneda = Usuario_Tiene_Moneda.query.filter_by(id_usuario=id_usuario).first()
	if usuario_tiene_moneda is None:
		return jsonify({'message': 'La cuenta no existe'}), 404
	usuario_tiene_moneda.delete()
	return jsonify({'usuario_tiene_moneda': usuario_tiene_moneda})



@app.route('/api/v1/moneda', methods=['GET'])
def get_monedas():
	monedas = [ moneda.json() for moneda in Moneda.query.all() ] 
	return jsonify({'moneda': monedas})

@app.route('/api/v1/moneda/<id>', methods=['GET'])
def get_moneda(id):
	moneda = Moneda.query.filter_by(id=id).first()
	if moneda is None:
		return jsonify({'message': 'La moneda no existe'}), 404
	return jsonify({'moneda': moneda.json() })

@app.route('/api/v1/moneda/', methods=['POST'])
def create_moneda():
	json = request.get_json(force=True)
	if json.get('nombre') is None or json.get('sigla') is None:
		return jsonify({'message': 'El formato está mal'}), 400
	moneda = Moneda.create(json['id'],json['nombre'],json['sigla'])
	return jsonify({'moneda': moneda.json() })

@app.route('/api/v1/moneda/<id>', methods=['PUT'])
def update_moneda(id):
	moneda = Moneda.query.filter_by(id=id).first()
	if moneda is None:
		return jsonify({'message': 'La moneda no existe'}), 404
	json = request.get_json(force=True)

	if json.get('id') is None or json.get('nombre') is None or json.get('sigla') is None:
		return jsonify({'message': 'Solicitud Incorrecta'}), 400

	moneda.id = json['id']
	moneda.update()
	return jsonify({'moneda': moneda.json()})

@app.route('/api/v1/moneda/<id>', methods=['DELETE'])
def delete_moneda(id):
	moneda = Moneda.query.filter_by(id=id).first()
	if moneda is None:
		return jsonify({'message': 'la moneda no existe'}), 404
	moneda.delete()
	return jsonify({'moneda': moneda.json() })



@app.route('/api/v1/precio_moneda', methods=['GET'])
def get_precio_monedas():
	precios = [ precio_moneda.json() for precio_moneda in Precio_Moneda.query.all() ] 
	return jsonify({'precio_moneda': precios})

@app.route('/api/v1/precio_moneda/<id_moneda>', methods=['GET'])
def get_precio_moneda(id_moneda):
	precio_moneda = Precio_Moneda.query.filter_by(id_moneda=id_moneda).first()
	if precio_moneda is None:
		return jsonify({'message': 'La moneda no existe'}), 404
	return jsonify({'precio_moneda': precio_moneda.json() })

@app.route('/api/v1/precio_moneda/', methods=['POST'])
def create_precio_moneda():
	json = request.get_json(force=True)
	if json.get('fecha') is None or json.get('valor') is None or json.get('id_moneda') is None:
		return jsonify({'message': 'El formato está mal'}), 400

	precio_moneda = Precio_Moneda.create(json['fecha'],json['valor'],json['id_moneda'])
	return jsonify({'precio_moneda': precio_moneda.json() })

@app.route('/api/v1/precio_moneda/<id_moneda>', methods=['PUT'])
def update_precio_moneda(id_moneda):
	precio_moneda = Precio_Moneda.query.filter_by(id_moneda=id_moneda).first()
	if precio_moneda is None:
		return jsonify({'message': 'La moneda no existe'}), 404
	json = request.get_json(force=True)

	if json.get('id_moneda') is None or json.get('fecha') is None or json.get('valor') is None:
		return jsonify({'message': 'Solicitud Incorrecta'}), 400

	precio_moneda.id_moneda = json['id_moneda']
	precio_moneda.update()
	return jsonify({'precio_moneda': precio_moneda.json()})

@app.route('/api/v1/precio_moneda/<id_moneda>', methods=['DELETE'])
def delete_precio_moneda(id_moneda):
	precio_moneda = Precio_Moneda.query.filter_by(id_moneda=id_moneda).first()
	if precio_moneda is None:
		return jsonify({'message': 'el precio no existe'}), 404
	precio_moneda.delete()
	return jsonify({'precio_moneda': precio_moneda.json() })

######################## Consultas ########################

@app.route('/api/v1/consultas/1/<anno>', methods=['GET'])
def consulta1(anno):
	usuarios_registro = [ (usuario.nombre,usuario.apellido,usuario.fecha_registro) for usuario in db.session.query(Usuario).filter(extract('year', Usuario.fecha_registro) == anno).all()]
	return jsonify({'Usuarios registrados durante el año dado': usuarios_registro })

@app.route('/api/v1/consultas/2/<valor>', methods=['GET'])
def consulta2(valor):
	cuentas_bancarias = [ (cuenta_bancaria.numero_cuenta,cuenta_bancaria.balance) for cuenta_bancaria in db.session.query(Cuenta_Bancaria).filter(Cuenta_Bancaria.balance > valor).order_by(Cuenta_Bancaria.balance.asc()).all()]
	return jsonify({'Cuentas bancarias con balance superior al dado': cuentas_bancarias })

@app.route('/api/v1/consultas/3/<pais>', methods=['GET'])
def consulta3(pais):
	usuarios_pais = [ (pais.nombre,usuario.nombre,usuario.apellido) for usuario,pais in db.session.query(Usuario,Pais).join(Pais, Usuario.pais == Pais.cod_pais).filter(Pais.nombre == pais).all()]
	return jsonify({'Usuarios que pertenecen al país': usuarios_pais })

@app.route('/api/v1/consultas/4/<nombre>', methods=['GET'])
def consulta4(nombre):
	maximo_valor = [ (moneda.nombre,precio_moneda.valor) for moneda,precio_moneda in db.session.query(Moneda,Precio_Moneda).join(Precio_Moneda, Moneda.id == Precio_Moneda.id_moneda).filter(Moneda.nombre == nombre).order_by(Precio_Moneda.valor.desc()).limit(1).all()]
	return jsonify({'Máximo valor histórico': maximo_valor })

@app.route('/api/v1/consultas/5/<sigla>', methods=['GET']) #Me falta sumar :3c
def consulta5(sigla):
	cantidad_monedas = [ (moneda.sigla,db.func.sum(usuario_tiene_moneda.balance)) for moneda,usuario_tiene_moneda in db.session.query(Moneda,Usuario_Tiene_Moneda).join(Usuario_Tiene_Moneda, Moneda.id == Usuario_Tiene_Moneda.id_moneda).filter(Moneda.sigla == sigla).all()]
	#db.session.query(Moneda.sigla,func.sum(Usuario_Tiene_Moneda.balance)).join(Usuario_Tiene_Moneda, Moneda.id == Usuario_Tiene_Moneda.id_moneda).filter(Moneda.sigla == sigla).group_by(Moneda.sigla).all()
	return jsonify({'Cantidad de monedas': cantidad_monedas })

if __name__ == '__main__':
	app.run(debug=True)
