#!/usr/bin/python3
# -*- coding: latin-1 -*-
import os
import sys
# import psycopg2
import json
from bson import json_util
from pymongo import MongoClient
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash


def create_app():
    app = Flask(__name__)
    return app

app = create_app()

# REPLACE WITH YOUR DATABASE NAME
MONGODATABASE = "prueba"
MONGOSERVER = "localhost"
MONGOPORT = 27017
client = MongoClient(MONGOSERVER, MONGOPORT)
mongodb = client[MONGODATABASE]

 # Uncomment for postgres connection
# REPLACE WITH YOUR DATABASE NAME, USER AND PASS


#Cambiar por Path Absoluto en el servidor
QUERIES_FILENAME = '/var/www/flaskr/queries'


@app.route("/")
def home():
    with open(QUERIES_FILENAME, 'r', encoding='utf-8') as queries_file:
        json_file = json.load(queries_file)
        pairs = [(x["name"],
                  x["database"],
                  x["description"],
                  x["query"]) for x in json_file]
        return render_template('file.html', results=pairs)


@app.route("/mongo", methods=['GET', 'POST'])
def mongo():
    query = request.args.get('query')
    #r = eval('mongodb.collectionprueba.createIndex({"contenido":"text"})')
    results = eval('mongodb.'+query)
    results = json_util.dumps(results, sort_keys=True, indent=4)
    if "find" in query:
        return results
    else:
        return "ok"

@app.route("/postgres")
def postgres():
    #query = request.args.get("query")
    query = "SELECT * FROM Restaurantes"
    cursor = postgresdb.cursor()
    cursor.execute(query)
    results = [[a for a in result] for result in cursor]
    return results



@app.route("/example")
def example():
    return render_template('example.html')


if __name__ == "__main__":
    app.run()
