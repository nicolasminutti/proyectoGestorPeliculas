# -*- coding: utf-8 -*-

import sqlite3
from sqlite3 import Error

class Pelicula:

    def abrirConexion(self):
        conexion = sqlite3.connect('videoteca.db')
        sql = "CREATE TABLE IF NOT EXISTS 'peliculas'('id' INTEGER PRIMARY KEY AUTOINCREMENT, 'titulo' TEXT(40) NOT NULL, 'categoria' TEXT(30) NOT NULL, 'fecha' INT(4) NOT NULL, 'director' TEXT(30) NOT NULL, 'sinopsis' TEXT(60) NOT NULL)"
        sql1 = "CREATE TABLE IF NOT EXISTS 'categoria'('descripcion' TEXT(30) NOT NULL)"
        conexion.execute(sql)
        conexion.execute(sql1)
        return conexion
    
    def consultaCategoria(self):
        try:
            conexion = self.abrirConexion()
            cursor = conexion.cursor()
            sql = 'SELECT descripcion FROM categoria'
            cursor.execute(sql)
            data = []
            for row in cursor.fetchall():
                data.append(row[0])
            return data
    
        except Error as err:
            print('Falló la conexión: %s\nError: %s' % (sql, str(err)))

        finally:
            conexion.close()

    def altaPelicula(self, datos):
        try:
            conexion = self.abrirConexion()
            cursor = conexion.cursor()
            sql = 'INSERT INTO peliculas(titulo, categoria, fecha, director, sinopsis) VALUES (?, ?, ?, ?, ?)'
            cursor.execute(sql, datos)
            conexion.commit()
            conexion.close()

        except Error as err:
            print('Falló la conexión: %s\nError: %s' % (sql, str(err)))
        
        finally:
            conexion.close()

    def consultaPelicula(self, datos):
        try:
            conexion = self.abrirConexion()
            cursor = conexion.cursor()
            sql = 'SELECT titulo, categoria, fecha, director, sinopsis FROM peliculas WHERE id = ?'
            cursor.execute(sql, datos)
            return cursor.fetchall()

        except Error as err:
            print('Falló la conexión: %s\nError: %s' % (sql, str(err)))

        finally:
            conexion.close()

    def recuperaTodas(self):
        try:
            conexion = self.abrirConexion()
            cursor = conexion.cursor()
            sql = 'SELECT * FROM peliculas'
            cursor.execute(sql)
            return cursor.fetchall()
        
        except Error as err:
            print('Falló la conexión: %s\nError: %s' % (sql, str(err)))

        finally:
            conexion.close()

    def bajaPelicula(self, datos):
        try:
            conexion = self.abrirConexion()
            cursor = conexion.cursor()
            sql = 'DELETE FROM peliculas WHERE id = ?'
            cursor.execute(sql, datos)
            conexion.commit()
            return cursor.rowcount

        except Error as err:
            print('Falló la conexión: %s\nError: %s' % (sql, str(err)))
        
        finally:
            conexion.close()

    def modificaPelicula(self, datos):
        try:
            conexion = self.abrirConexion()
            cursor = conexion.cursor()
            sql = "UPDATE peliculas SET 'titulo' = ?, 'categoria' = ?, 'fecha' = ?, 'director' = ?, 'sinopsis' = ? WHERE id = ?"
            cursor.execute(sql, datos)
            conexion.commit()
            return cursor.rowcount

        except Error as err:
            print('Falló la conexión: %s\nError: %s' % (sql, str(err)))

        finally:
            conexion.close()

    def consultaAvanzada(self, datos):
        try:
            conexion = self.abrirConexion()
            cursor = conexion.cursor()
            cursor.execute(datos)
            return cursor.fetchall()

        except Error as err:
            print('Falló la conexión: %s\nError: %s' % (sql, str(err)))

        finally:
            conexion.close()