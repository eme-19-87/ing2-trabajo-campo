<?php

namespace App\Controllers;

use CodeIgniter\Entity\Cast\StringCast;
use CodeIgniter\HTTP\Request;
use CodeIgniter\Session\Session;
use App\Models\Products;
use App\Models\GeneroModel;
use App\Models\AutorModel;
use App\Models\EditorialModel;
use App\Models\LibroModel;

class ProductController extends BaseController{
    /**
     * Constructor de la clase ProductController
     */
    public function __construct()
    {
        //llamada al constructor de la superclase
        parent::__construct();   
       
    }
    public function show_product_form(){
       
        //creo los modelos para recuperar la información de generos, autores y editoriales
        $generoModel = new GeneroModel(); 
        $autorModel=new AutorModel();
        $editorialModel=new EditorialModel();

        //llamo a los métodos pertinentes para obtener los datos
        $generos = $generoModel->getGeneros();
        $autores=$autorModel->getAutores();
        $editoriales=$editorialModel->getEditoriales();

        //cargo la vista
        return view('plantillas/head') .
        view('plantillas/navbar') .
        view('contenido/ProductAdmin',['generos' => $generos,'editoriales'=>$editoriales,'autores'=>$autores]) .
        view('plantillas/footer');
    }

    public function create_book()
    {
        //el helper ayuda al control de errores.
        helper(['form']);

        // creo el objeto para la validación del formulario
        $validation = \Config\Services::validation();
        //la validación se encuentra en app->Config->Validation.php
        $validation->setRuleGroup('newBook'); 

        //compruebo si se cumplen las reglas establecidas en el conjunto de reglas newBook
        if (!$validation->withRequest($this->request)->run()) {
            ///si no se cumplen, redirijo a la vista del formulario con los msjs de error
            return redirect()->back()->withInput()->with('errors', $validation->getErrors());
        }

        //creo el conjunto de datos que voy a pasar al modelo para realizar la consulta
        //con $this->request->getPost obtengo los datos de los inpunt según su valor
        //en el atributo name
        $datos = [
            'titulo' => $this->request->getPost('nombre_libro'),
            'precio' => floatval($this->request->getPost('precio_libro')),
            'editorial_id' => intval($this->request->getPost('editorial_libro')),
            'sinopsis' => $this->request->getPost('sinopsis_libro'),
            'paginas' => intval($this->request->getPost('paginas_libro')),
            'autor_id' => intval($this->request->getPost('autor_libro')),
            'genero_id' => intval($this->request->getPost('genero_libro')),
            'fecha_publicacion' =>date('Y-m-d', strtotime( $this->request->getPost('fecha_libro'))) 
        ];
        //creo una instancia del modelo LibroModel
        $libroModel = new LibroModel();
        //llamo al método para crear el nuevo libro
        $resultado=$libroModel->crearLibro($datos);

        //este tiene dos campos: el resultado que será 0 si hay error, 1 en caso contrario
        //si no hubo error, retorno a la vista del formulario para cargar un nuevo libro
        if ($resultado['resultado']){
            return redirect()->to(base_url('products'))->with('correct_insert',"Libro insertado correctamente");
        }else{
            //si el resultado fue 0, mando el mensaje de error a la vista
            return redirect()->to(base_url('products'))->with('error_insert', $resultado['msj_error']);
        }
       
        //return redirect()->to('/libros')->with('mensaje', 'Libro cargado correctamente.');
    }
}  