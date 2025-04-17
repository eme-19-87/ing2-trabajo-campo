<?php

namespace App\Controllers;

use CodeIgniter\Entity\Cast\StringCast;
use CodeIgniter\HTTP\Request;
use CodeIgniter\Session\Session;
use App\Models\Products;
use App\Models\GeneroModel;

class ProductController extends BaseController{
    public function show_product_form(){
        $generoModel = new GeneroModel();
        $generos = $generoModel->obtenerGeneros();
        return view('plantillas/head') .
        view('plantillas/navbar') .
        view('contenido/ProductAdmin',['generos' => $generos]) .
        view('plantillas/footer');
    }
}  