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
       
     
        $generoModel = new GeneroModel(); 
        $autorModel=new AutorModel();
        $editorialModel=new EditorialModel();
        $generos = $generoModel->obtenerGeneros();
        $autores=$autorModel->obtenerAutores();
        $editoriales=$editorialModel->obtenerEditoriales();
        return view('plantillas/head') .
        view('plantillas/navbar') .
        view('contenido/ProductAdmin',['generos' => $generos,'editoriales'=>$editoriales,'autores'=>$autores]) .
        view('plantillas/footer');
    }

    public function create_book()
    {
        helper(['form']);

        // Validaciones (asumimos que están hechas aparte)
        $validation = \Config\Services::validation();
        $validation->setRuleGroup('newBook'); // Validación separada

        if (!$validation->withRequest($this->request)->run()) {
            //dd($validation->getErrors());
            return redirect()->back()->withInput()->with('errors', $validation->getErrors());
        }

        $datos = [
            'titulo' => $this->request->getPost('nombre_libro'),
            'precio' => $this->request->getPost('precio_libro'),
            'editorial_id' => $this->request->getPost('editorial_libro'),
            'sinopsis' => $this->request->getPost('sinopsis_libro'),
            'paginas' => $this->request->getPost('paginas_libro'),
            'autor_id' => $this->request->getPost('autor_libro'),
            'genero_id' => $this->request->getPost('genero_libro'),
            'fecha_publicacion' => $this->request->getPost('fecha_libro'),
        ];

        $libroModel = new LibroModel();
        $resultado=$libroModel->create_book($datos);
        if ($resultado){
            return "Libro ingresado con éxito";
        }else{
            return "Error al ingresar el libro";
        }
       
        //return redirect()->to('/libros')->with('mensaje', 'Libro cargado correctamente.');
    }
}  