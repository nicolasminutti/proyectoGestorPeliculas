# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import scrolledtext as st
import re
import datetime
import clase

class FormularioPelicula:
    def __init__(self):
        self.pelicula = clase.Pelicula()
        self.ventana = tk.Tk()
        self.ventana.title('Videoteca')
        self.ventana.wm_iconbitmap(bitmap='img\clapperboard.ico')
        self.ventana.resizable(0,0)
        self.cuaderno = ttk.Notebook(self.ventana)
        self.cargaPelicula()
        self.consultaPorCodigo()
        self.listadoCompleto()
        self.borrarPelicula()
        self.modificaPelicula()
        self.buscadorAvanzado()
        self.cuaderno.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        self.ventana.mainloop()

    def cargaPelicula(self):
        self.paginaCarga = tk.Frame(self.cuaderno)
        self.altaImagen = tk.PhotoImage(file='img/agregar.png')
        self.cuaderno.add(self.paginaCarga, text='Alta Película', image=self.altaImagen, compound=tk.LEFT)
        self.labelframe = tk.LabelFrame(self.paginaCarga, text='Película')
        self.labelframe.grid(column=0, row=0, padx=5, pady=10, columnspan=4)
        self.labelTitulo = tk.Label(self.labelframe, text='Título')
        self.labelTitulo.grid(column=0, row=0, padx=4, pady=4, sticky='W')
        self.titulocarga = tk.StringVar()
        self.entrytitulo = tk.Entry(self.labelframe, textvariable=self.titulocarga, width=58)
        self.entrytitulo.grid(column=1, row=0, padx=4, pady=4, columnspan=4, sticky='W')
        self.limitarCaracteres(self.titulocarga, 40)
        self.labelCategoria = tk.Label(self.labelframe, text='Categoría')
        self.labelCategoria.grid(column=0, row=1, padx=4, pady=4, sticky='W')
        self.categoriacarga = tk.StringVar()
        self.entrycategoria = ttk.Combobox(self.labelframe, textvariable=self.categoriacarga, values=self.pelicula.consultaCategoria(), state='readonly', width=22)
        self.entrycategoria.current(4)
        self.entrycategoria.grid(column=1, row=1, padx=4, pady=4, sticky='W')
        self.labelAnio = tk.Label(self.labelframe, text='Año')
        self.labelAnio.grid(column=2, row=1, padx=4, pady=4, sticky='W')
        self.aniocarga = tk.StringVar()
        self.entryanio = tk.Entry(self.labelframe, textvariable=self.aniocarga, width=25)
        self.entryanio.grid(column=3, row=1, padx=4, pady=4, sticky='W')
        self.limitarCaracteres(self.aniocarga, 4)
        self.labelDirector = tk.Label(self.labelframe, text='Director')
        self.labelDirector.grid(column=0, row=3, padx=4, pady=4, sticky='W')
        self.directorcarga = tk.StringVar()
        self.entrydirector = tk.Entry(self.labelframe, textvariable=self.directorcarga, width=58)
        self.entrydirector.grid(column=1, row=3, padx=4, pady=4, columnspan=4, sticky='W')
        self.limitarCaracteres(self.directorcarga, 30)
        self.labelSinopsis = tk.Label(self.labelframe, text='Sinopsis')
        self.labelSinopsis.grid(column=0, row=4, padx=4, pady=4, sticky='W')
        self.sinopsiscarga = tk.StringVar()
        self.entrysinopsis = tk.Entry(self.labelframe, textvariable=self.sinopsiscarga, width=58)
        self.entrysinopsis.grid(column=1, row=4, padx=4, pady=4, columnspan=4, sticky='W')
        self.limitarCaracteres(self.sinopsiscarga, 60)
        self.botonConfirma = tk.Button(self.labelframe, text='Confirmar', command=self.agregaPelicula)
        self.botonConfirma.grid(column=1, row=7, padx=4, pady=4, sticky='W')
        self.botonLimpiar = tk.Button(self.labelframe, text='  Limpiar  ', command=self.btnLimpiarEntry)
        self.botonLimpiar.grid(column=1, row=7, padx=4, pady=4, sticky='E')

    def limitarCaracteres(self, entrada, largo):
        def callback(entrada):
            c = entrada.get()[0:largo]
            entrada.set(c)
        entrada.trace('w', lambda name, index, mode, entrada=entrada: callback(entrada))

    def agregaPelicula(self):
        titulo = re.fullmatch(r'[A-Za-z0-9ÁÉÍÓÚÜÑÇáéíóúüñç\s\-,.]+$', self.titulocarga.get())
        anio = re.fullmatch(r'(18[89][089]|19\d\d|20[01][0-9])', self.aniocarga.get())
        director = re.fullmatch(r'[A-Za-zÁÉÍÓÚÜÑÇáéíóúüñç\s\-]+$', self.directorcarga.get())
        diccionario = {'Título': titulo, 'Año': anio, 'Director': director}
        lista = []
        for key in diccionario:
            if diccionario[key] is None:
                lista.append(key)
        if len(lista) != 0:
            mb.showinfo('Atención', 'Verifique que no estén vacíos\no tengan caracteres inválidos\nlos siguientes campos: %s' % ', '.join(lista))
        if len(lista) == 0:
            datos = (self.titulocarga.get(), self.categoriacarga.get(), self.aniocarga.get(), self.directorcarga.get(), self.sinopsiscarga.get())
            self.pelicula.altaPelicula(datos)
            mb.showinfo('Información', 'Los datos fueron cargados')
            self.titulocarga.set(''),
            self.sinopsiscarga.set('')
            self.aniocarga.set('')
            self.directorcarga.set('')
        del lista

    def btnLimpiarEntry(self):
        result = mb.askokcancel(
            'Información', '¿Está seguro de borrar el formulario?')
        if result:
            self.entrycategoria.current(4)
            self.titulocarga.set(''),
            self.sinopsiscarga.set('')
            self.aniocarga.set('')
            self.directorcarga.set('')

    def consultaPorCodigo(self):
        self.paginaConsulta = tk.Frame(self.cuaderno)
        self.consultaImagen = tk.PhotoImage(file='img/buscar.png')
        self.cuaderno.add(self.paginaConsulta, text='Consulta por Id', image=self.consultaImagen, compound=tk.LEFT)
        self.labelframe = tk.LabelFrame(self.paginaConsulta, text='Consulta')
        self.labelframe.grid(column=0, row=0, padx=5, pady=10, columnspan=4)
        self.labelId = tk.Label(self.labelframe, text='Id Película')
        self.labelId.grid(column=0, row=0, padx=4, pady=4, sticky='W')
        self.id = tk.StringVar()
        self.entryid = tk.Entry(self.labelframe, textvariable=self.id)
        self.entryid.grid(column=1, row=0, padx=4, pady=4, sticky='W')
        self.labeltituloConsulta = tk.Label(self.labelframe, text='Título')
        self.labeltituloConsulta.grid(column=0, row=1, padx=4, pady=4, sticky='W')
        self.tituloConsulta = tk.StringVar()
        self.entrytituloConsulta = tk.Entry(self.labelframe, textvariable=self.tituloConsulta, state='readonly', width=58)
        self.entrytituloConsulta.grid(column=1, row=1, padx=4, pady=4, columnspan=4, sticky='W')
        self.labelCategoriaConsulta = tk.Label(self.labelframe, text='Categoría')
        self.labelCategoriaConsulta.grid(column=0, row=2, padx=4, pady=4, sticky='W')
        self.categoriaConsulta = tk.StringVar()
        self.entrycategoriaConsulta = tk.Entry(self.labelframe, textvariable=self.categoriaConsulta, state='readonly', width=25)
        self.entrycategoriaConsulta.grid(column=1, row=2, padx=4, pady=4, sticky='W')
        self.labelAnioConsulta = tk.Label(self.labelframe, text='Año')
        self.labelAnioConsulta.grid(column=2, row=2, padx=4, pady=4, sticky='W')
        self.anioConsulta = tk.StringVar()
        self.entryanioConsulta = tk.Entry(self.labelframe, textvariable=self.anioConsulta, state='readonly', width=25)
        self.entryanioConsulta.grid(column=3, row=2, padx=4, pady=4, sticky='W')
        self.labelDirectorConsulta = tk.Label(self.labelframe, text='Director')
        self.labelDirectorConsulta.grid(column=0, row=5, padx=4, pady=4, sticky='W')
        self.directorConsulta = tk.StringVar()
        self.entrydirectorConsulta = tk.Entry(self.labelframe, textvariable=self.directorConsulta, state='readonly', width=58)
        self.entrydirectorConsulta.grid(column=1, row=5, padx=4, pady=4, columnspan=4, sticky='W')
        self.labelSinopsisConsulta = tk.Label(self.labelframe, text='Sinopsis')
        self.labelSinopsisConsulta.grid(column=0, row=6, padx=4, pady=4, sticky='W')
        self.sinopsisConsulta = tk.StringVar()
        self.entrysinopsisConsulta = tk.Entry(self.labelframe, textvariable=self.sinopsisConsulta, state='readonly', width=58)
        self.entrysinopsisConsulta.grid(column=1, row=6, padx=4, pady=4, columnspan=4, sticky='W')
        self.botonConsulta = tk.Button(self.labelframe, text='Consultar', command=self.consulta)
        self.botonConsulta.grid(column=3, row=8, padx=4, pady=4)

    def consulta(self):
        datos = (self.id.get(), )
        respuesta = self.pelicula.consultaPelicula(datos)
        if len(respuesta) > 0:
            self.tituloConsulta.set(respuesta[0][0])
            self.categoriaConsulta.set(respuesta[0][1])
            self.anioConsulta.set(respuesta[0][2])
            self.directorConsulta.set(respuesta[0][3])
            self.sinopsisConsulta.set(respuesta[0][4])
        else:
            mb.showinfo('Información', 'El ID {} no existe\n¡Por favor verifique!'.format(*datos))

    def listadoCompleto(self):
        self.paginaListado = tk.Frame(self.cuaderno)
        self.listadoImagen = tk.PhotoImage(file='img/listar.png')
        self.cuaderno.add(self.paginaListado, text='Listado Películas', image=self.listadoImagen, compound=tk.LEFT)
        self.labelframe = tk.LabelFrame(self.paginaListado, text='Listado')
        self.labelframe.grid(column=0, row=0, padx=5, pady=10, columnspan=4)
        self.botonListado = tk.Button(self.labelframe, text='Listado completo', command=self.listar)
        self.botonListado.grid(column=0, row=0, padx=4, pady=4)
        self.tree = ttk.Treeview(self.labelframe, column=('column1', 'column2', 'column3', 'column4', 'column5', 'column6'), show='headings')
        self.yscrollbar = tk.Scrollbar(self.labelframe, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.yscrollbar.set)
        self.yscrollbar.grid(row=1, column=1, sticky='NSW')
        self.yscrollbar.configure(command=self.tree.yview)       
        self.tree.heading('#1', text='Id')
        self.tree.column('#1', width=30, anchor='center')
        self.tree.heading('#2', text='Título')
        self.tree.column('#2', width=170)
        self.tree.heading('#3', text='Categoría')
        self.tree.column('#3', width=100)
        self.tree.heading('#4', text='Año')
        self.tree.column('#4', width=50, anchor='center')
        self.tree.heading('#5', text='Director')
        self.tree.column('#5', width=150)
        self.tree.heading('#6', text='Sinopsis')
        self.tree.column('#6', width=150)
        self.tree.grid(column=0, row=1, padx=15, pady=15)

    def listar(self):
        listado = self.pelicula.recuperaTodas()
        if len(self.tree.get_children()) > 0:
            self.tree.delete(*self.tree.get_children())
        for row in listado:
            self.tree.insert('', tk.END, values=row)

    def borrarPelicula(self):
        self.paginaBorrar = tk.Frame(self.cuaderno)
        self.borrarImagen = tk.PhotoImage(file='img/borrar.png')
        self.cuaderno.add(self.paginaBorrar, text='Borrar Película', image=self.borrarImagen, compound=tk.LEFT)
        self.labelframe = tk.LabelFrame(self.paginaBorrar, text='Borrar Película')
        self.labelframe.grid(column=0, row=0, padx=5, pady=10, columnspan=4)
        self.labelBorrar = tk.Label(self.labelframe, text='Id Película')
        self.labelBorrar.grid(column=0, row=0, padx=4, pady=4, sticky='W')
        self.idBorrado = tk.StringVar()
        self.entryidBorrado = tk.Entry(self.labelframe, textvariable=self.idBorrado)
        self.entryidBorrado.grid(column=1, row=0, padx=20, pady=20, sticky='W')
        self.botonBorrar = tk.Button(self.labelframe, text='Borrar', command=self.borrar)
        self.botonBorrar.grid(column=1, row=1, padx=4, pady=4)

    def borrar(self):
        datos = (self.idBorrado.get(), )
        cantidad = self.pelicula.bajaPelicula(datos)
        if cantidad == 1:
            mb.showinfo('Información', 'Se borró la película con Id {}'.format(*datos))
        else:
            mb.showinfo('Información', 'No existe el ID {}'.format(*datos))

    def modificaPelicula(self):
        self.paginaModifica = tk.Frame(self.cuaderno)
        self.modificaImagen = tk.PhotoImage(file='img/editar.png')
        self.cuaderno.add(self.paginaModifica, text='Modificar Película', image=self.modificaImagen, compound=tk.LEFT)
        self.labelframe = tk.LabelFrame(self.paginaModifica, text='Modificar')
        self.labelframe.grid(column=0, row=0, padx=5, pady=10, columnspan=4)
        self.labelId = tk.Label(self.labelframe, text='Id Película')
        self.labelId.grid(column=0, row=0, padx=4, pady=4, sticky='W')
        self.idModifica = tk.StringVar()
        self.entryidModifica = tk.Entry(self.labelframe, textvariable=self.idModifica)
        self.entryidModifica.grid(column=1, row=0, padx=4, pady=4, sticky='W')
        self.labeltituloModifica = tk.Label(self.labelframe, text='Título')
        self.labeltituloModifica.grid(column=0, row=1, padx=4, pady=4, sticky='W')
        self.tituloModifica = tk.StringVar()
        self.limitarCaracteres(self.tituloModifica, 40)
        self.entrytituloModifica = tk.Entry(self.labelframe, textvariable=self.tituloModifica, state=tk.DISABLED, width=58)
        self.entrytituloModifica.grid(column=1, row=1, padx=4, pady=4, columnspan=4, sticky='W')
        self.labelcategoriaModifica = tk.Label(self.labelframe, text='Categoría')
        self.labelcategoriaModifica.grid(column=0, row=2, padx=4, pady=4, sticky='W')
        self.categoriaModifica = tk.StringVar()
        self.entrycategoriaModifica = ttk.Combobox(self.labelframe, textvariable=self.categoriaModifica, values=self.pelicula.consultaCategoria(), state=tk.DISABLED, width=22)
        self.entrycategoriaModifica.grid(column=1, row=2, padx=4, pady=4, sticky='W')
        self.labelanioModifica = tk.Label(self.labelframe, text='Año')
        self.labelanioModifica.grid(column=2, row=2, padx=4, pady=4, sticky='W')
        self.anioModifica = tk.StringVar()
        self.limitarCaracteres(self.anioModifica, 4)
        self.entryanioModifica = tk.Entry(self.labelframe, textvariable=self.anioModifica, state=tk.DISABLED, width=25)
        self.entryanioModifica.grid(column=3, row=2, padx=4, pady=4, sticky='W')
        self.labeldirectorModifica = tk.Label(self.labelframe, text='Director')
        self.labeldirectorModifica.grid(column=0, row=5, padx=4, pady=4, sticky='W')
        self.directorModifica = tk.StringVar()
        self.limitarCaracteres(self.directorModifica, 30)
        self.entrydirectorModifica = tk.Entry(self.labelframe, textvariable=self.directorModifica, state=tk.DISABLED, width=58)
        self.entrydirectorModifica.grid(column=1, row=5, padx=4, pady=4, columnspan=4, sticky='W')
        self.labelsinopsisModifica = tk.Label(self.labelframe, text='Sinopsis')
        self.labelsinopsisModifica.grid(column=0, row=6, padx=4, pady=4, sticky='W')
        self.sinopsisModifica = tk.StringVar()
        self.limitarCaracteres(self.sinopsisModifica, 60)
        self.entrysinopsisModifica = tk.Entry(self.labelframe, textvariable=self.sinopsisModifica, state=tk.DISABLED, width=58)
        self.entrysinopsisModifica.grid(column=1, row=6, padx=4, pady=4, columnspan=4, sticky='W')
        self.botonConsulta = tk.Button(self.labelframe, text='Consultar', command=self.modifica)
        self.botonConsulta.grid(column=1, row=7, padx=4, pady=4, sticky='W')
        self.botonConsulta = tk.Button(self.labelframe, text='Modificar', command=self.guardaModificacion)
        self.botonConsulta.grid(column=1, row=7, padx=4, pady=4, sticky='E')

    def modifica(self):
        datos = (self.idModifica.get(), )
        respuesta = self.pelicula.consultaPelicula(datos)
        if len(respuesta) > 0:
            self.entrytituloModifica.config(state=tk.NORMAL)
            self.tituloModifica.set(respuesta[0][0])
            self.entrycategoriaModifica.config(state=tk.NORMAL)
            self.categoriaModifica.set(respuesta[0][1])
            self.entryanioModifica.config(state=tk.NORMAL)
            self.anioModifica.set(respuesta[0][2])
            self.entrydirectorModifica.config(state=tk.NORMAL)
            self.directorModifica.set(respuesta[0][3])
            self.entrysinopsisModifica.config(state=tk.NORMAL)
            self.sinopsisModifica.set(respuesta[0][4])
        else:
            mb.showinfo('Información', 'No existe el ID {}\nIntroduzca el ID nuevamente'.format(*datos))

    def guardaModificacion(self):
        titulo = re.fullmatch(r'[A-Za-z0-9ÁÉÍÓÚÜÑÇáéíóúüñç\s\-,.]+$', self.tituloModifica.get())
        anio = re.fullmatch(r'(18[89][089]|19\d\d|20[01][0-9])', self.anioModifica.get())
        director = re.fullmatch(r'[A-Za-zÁÉÍÓÚÜÑÇáéíóúüñç\s\-]+$', self.directorModifica.get())
        diccionarioModificado = {'Título': titulo, 'Año': anio, 'Director': director}
        listaModificada = []
        for key in diccionarioModificado:
            if diccionarioModificado[key] is None:
                listaModificada.append(key)
        if len(listaModificada) != 0:
            mb.showinfo('Atención', 'Verifique que no estén vacíos\no tengan caracteres inválidos\nlos siguientes campos: %s' % ', '.join(listaModificada))
        if len(listaModificada) == 0:
            datos = self.tituloModifica.get(), self.categoriaModifica.get(), self.anioModifica.get(), self.directorModifica.get(), self.sinopsisModifica.get(), (self.idModifica.get())
            self.pelicula.modificaPelicula(datos)
            mb.showinfo('Información', 'Los datos fueron cargados')
            self.tituloModifica.set(''),
            self.sinopsisModifica.set('')
            self.anioModifica.set('')
            self.directorModifica.set('')
        del listaModificada

    def buscadorAvanzado(self):
        self.paginaconsultaAvanzada = tk.Frame(self.cuaderno)
        self.consultaAvanzadaImagen = tk.PhotoImage(file='img/avanzado.png')
        self.cuaderno.add(self.paginaconsultaAvanzada, text='Consulta Avanzada', image=self.consultaAvanzadaImagen, compound=tk.LEFT)
        self.labelframe = tk.LabelFrame(self.paginaconsultaAvanzada, text='Consulta Avanzada')
        self.labelframe.grid(column=0, row=0, padx=5, pady=10, columnspan=4)
        self.labeltextoBuscar = tk.Label(self.labelframe, text='Texto buscado')
        self.labeltextoBuscar.grid(column=0, row=0, padx=4, pady=4, sticky='W')
        self.textoBuscar = tk.StringVar()
        self.limitarCaracteres(self.textoBuscar, 15)
        self.entrytextoBuscar = tk.Entry(self.labelframe, textvariable=self.textoBuscar, width=20)
        self.entrytextoBuscar.grid(column=1, row=0, padx=4, pady=4, columnspan=4, sticky='W')
        self.labelbuscarDonde = tk.Label(self.labelframe, text='¿Dónde buscar?')
        self.labelbuscarDonde.grid(column=0, row=1, padx=4, pady=4, sticky='W')
        self.tituloCheck = tk.StringVar()
        self.optiontituloCheck = tk.Checkbutton(self.labelframe, text='Título', variable=self.tituloCheck, onvalue='titulo', offvalue='')
        self.optiontituloCheck.grid(column=1, row=1, padx=4, pady=4, sticky='W')
        self.directorCheck = tk.StringVar()
        self.optiondirectorCheck = tk.Checkbutton(self.labelframe, text='Director', variable=self.directorCheck, onvalue='director', offvalue='')
        self.optiondirectorCheck.grid(column=2, row=1, padx=4, pady=4, sticky='W')
        self.sinopsisCheck = tk.StringVar()
        self.optionsinopsisCheck = tk.Checkbutton(self.labelframe, text='Sinopsis', variable=self.sinopsisCheck, onvalue='sinopsis', offvalue='')
        self.optionsinopsisCheck.grid(column=3, row=1, padx=4, pady=4, sticky='W')
        self.botonConsulta = tk.Button(self.labelframe, text='Buscar', command=self.buscarAvanzado)
        self.botonConsulta.grid(column=5, row=1, padx=4, pady=4)
        self.labelframeListado = tk.LabelFrame(self.paginaconsultaAvanzada, text='Listado')
        self.labelframeListado.grid(column=1, row=2, padx=5, pady=10, columnspan=4)
        self.treeListado = ttk.Treeview(self.labelframeListado, column=('column1', 'column2', 'column3', 'column4', 'column5', 'column6'), show='headings')
        self.treeListado.grid(column=0, row=0, padx=4, pady=4)
        self.yscrollbarListado = tk.Scrollbar(self.labelframeListado, orient='vertical', command=self.treeListado.yview)
        self.treeListado.configure(yscrollcommand=self.yscrollbarListado.set)
        self.yscrollbarListado.grid(column=1, row=1, sticky='NSW')
        self.yscrollbarListado.configure(command=self.treeListado.yview)       
        self.treeListado.heading('#1', text='Id')
        self.treeListado.column('#1', width=30, anchor='center')
        self.treeListado.heading('#2', text='Título')
        self.treeListado.column('#2', width=170)
        self.treeListado.heading('#3', text='Categoría')
        self.treeListado.column('#3', width=100)
        self.treeListado.heading('#4', text='Año')
        self.treeListado.column('#4', width=50, anchor='center')
        self.treeListado.heading('#5', text='Director')
        self.treeListado.column('#5', width=150)
        self.treeListado.heading('#6', text='Sinopsis')
        self.treeListado.column('#6', width=150)
        self.treeListado.grid(column=0, row=1, padx=15, pady=15)
        
    def buscarAvanzado(self):
        try:
            tituloBuscado = re.fullmatch(r'[A-Za-z0-9ÁÉÍÓÚÜÑÇáéíóúüñç\s\-,.]+$', self.textoBuscar.get())

        except:
            tituloBuscado = None
        
        if self.textoBuscar.get() == '' or tituloBuscado == None:
            mb.showinfo('Atención', 'Debe completar el texto a buscar y/o\nverifique no tenga caracteres inválidos')
            self.entrytextoBuscar.focus()
        else:
            listado = [self.textoBuscar.get(), self.tituloCheck.get(), self.directorCheck.get(), self.sinopsisCheck.get()]
            consulta = 'SELECT * FROM peliculas WHERE '
            liketextoBuscar = ' LIKE "%' + (listado[0]) + '%"'
            listado.pop(0)
            listado = [item for item in listado if item]
            wheretextoBuscar = '||'.join(listado)
            if len(listado) > 0:
                datos = (consulta + wheretextoBuscar + liketextoBuscar)
                respuesta = (self.pelicula.consultaAvanzada(datos)) 
                if len(self.pelicula.consultaAvanzada(datos)) == 0:
                    mb.showinfo('Atención', 'No hay coicidencias')
                else:
                    if len(self.treeListado.get_children()) > 0:
                        self.treeListado.delete(*self.treeListado.get_children())
                    for row in respuesta:
                        self.treeListado.insert('', tk.END, values=row)
            else:
                mb.showinfo('Atención', 'Debe seleccionar al menos una opción')
        del listado

aplicacion = FormularioPelicula()