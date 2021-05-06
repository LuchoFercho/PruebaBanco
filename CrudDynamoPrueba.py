import boto3
from botocore.exceptions import ClientError
from pprint import pprint
import json
from CreateUsersTable import create_users_table

# Funcion para agregar elementos a tabla Users
def put_user(userid, username, age, dynamodb=None):
    # coneccion a la base de datos utilizando boto3
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000",
                                    region_name="sa-east-1",
                                    aws_access_key_id="AKIAYSBMQCN7NPTKWMM4",
                                    aws_secret_access_key="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")

    table = dynamodb.Table('Users')
    response = table.put_item(
       Item={
            'userid': userid,
            'username': username,
            'info': {
                'age': age,
            }
        }
    )
    return response

# Funcion para leer elementos de la tabla Users
def get_user(userid, username, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('Users')

    try:
        response = table.get_item(Key={'userid': userid, 'username': username})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response


# Funcion para actualizar elementos de la tabla Users
def update_user(userid, username, age, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('Users')

    response = table.update_item(
        Key={
            'userid': userid,
            'username': username
        },
        UpdateExpression="set info.age=:a",
        ExpressionAttributeValues={
            ':a': age
        },
        ReturnValues="UPDATED_NEW"
    )
    return response


# Funciono para eliminar elementos de la tabla Users
def delete_user(userid, username, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('Users')

    try:
        response = table.delete_item(
            Key={
                'userid': userid,
                'username': username
            }
        )
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print(e.response['Error']['Message'])
        else:
            raise
    else:
        return response



def crud_dynamo_banc(accion,userid,username,age):
    respuesta={}
    if accion == "crear tabla":
        create_users_table()
    elif accion == 'agregar':
        try:
            agregarUsuario=put_user(userid,username,age)
            # agregarUsuario=put_user(200,"Luis",22)
            print("usuario Agregado")
            respuesta['accion']="Usuario Agregado"
            respuesta['userid']=userid
            respuesta['username']=username
            respuesta['age']=age
            with open('respuesta.json', 'w') as file:
                json.dump({'json': respuesta}, file)
            return respuesta
        except Exception as error:
            print("|Error|",error)
            return r_500
        
    elif accion == 'leer':
        try:
            leerUsuario=get_user(userid,username)
            print("usuario leido")
            if 'Item' in leerUsuario:
                respuesta['accion']="Usuario leido"
                respuesta['userid']=userid
                respuesta['username']=username
                respuesta['info']=str(leerUsuario['Item']['info'])
            else:
                respuesta['info']="el usuario no existe"
                # se crea un archivo Json para ser retornado con la respuesta
                with open('respuesta.json', 'w') as file:
                    json.dump({'json': respuesta}, file)
            return respuesta
        except Exception as error:
            print("|Error|",error)
            return r_500
    elif accion == "actualizar":
        try:
            actualizarUsuario=update_user(userid,username,age)
            print("usuario actualizado")
            if 'Attributes' in actualizarUsuario:
                respuesta['accion']="Usuario Actualizado"
                respuesta['userid']=userid
                respuesta['username']=username
                respuesta['age']=age
            else:
                respuesta['info']="el usuario no existe"
            with open('respuesta.json', 'w') as file:
                json.dump({'json': respuesta}, file)
            return respuesta
        except Exception as error:
            print("|Error|",error)
            return error
    elif accion == "eliminar":
        try:
            eliminarUsuario=delete_user(userid,username)
            if 'ConsumedCapacity' not in eliminarUsuario:
                print("usuario eliminado")
                respuesta['accion']="Usuario eliminado"
                respuesta['userid']=userid
                respuesta['username']=username
            else:
                respuesta['info']="el usuario no existe"
            with open('respuesta.json', 'w') as file:
                json.dump({'json': respuesta}, file)
            return respuesta
        except Exception as error:
            print("|Error|",error)
            return error


if __name__ == '__main__':
    # firstUser=put_user(999,"Luis" , 20)
    # pprint(firstUser, sort_dicts=False)

    # userUpdate=update_user(999,"luis",21)
    # deleteUser=delete_user(996,"Fransisco")

    #userRead = get_user(210,"Manuel")
    #pprint(userRead,sort_dicts=False)

    probando = crud_dynamo_banc("crear tabla",4410,"Juanse",100)
    pprint(probando)

