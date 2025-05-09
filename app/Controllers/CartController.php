<?php

namespace App\Controllers;

use CodeIgniter\Entity\Cast\StringCast;
use CodeIgniter\HTTP\Request;
use CodeIgniter\Session\Session;
use App\Models\Products;
use App\Models\GeneroModel;
use App\Models\AutorModel;
use App\Models\EditorialModel;
use App\Models\ArticuloModel;
use ci4shoppingcart\Libraries\Cart;

class CartController extends BaseController{
    private $cart;
    /**
     * Constructor de la clase ProductController
     */
    public function __construct()
    {
        //llamada al constructor de la superclase
        parent::__construct(); 
        $this->cart=new Cart();  
    }

    public function show_cart(){
        $cart_data=$this->get_cart();
        return view('plantillas/head') .
        view('plantillas/navbar') .
        view('contenido/VistaCarrito',['cart' => $cart_data]) .
        view('plantillas/footer');
        
    }

    /**
     * Permite obtener los datos guardados en el carrito
     */
    private function get_cart(){
        return $this->cart->contents();
    }


    /**
     * Permite agregar un nuevo producto al carrito
     */
    public function add_item_to_cart($id_prod){
        //el helper ayuda al control de errores.
        //helper(['form']);

        // creo el objeto para la validación del formulario
        //$validation = \Config\Services::validation();
        //la validación se encuentra en app->Config->Validation.php
        //$validation->setRuleGroup('newBook'); 

        //compruebo si se cumplen las reglas establecidas en el conjunto de reglas newBook
        //if (!$validation->withRequest($this->request)->run()) {
            ///si no se cumplen, redirijo a la vista del formulario con los msjs de error
            //return redirect()->back()->withInput()->with('errors', $validation->getErrors());
        //} 
        $productoExiste = false;

        //controla que el producto ya no esté en el carrito
        foreach ($this->get_cart() as $item) {
            if ($item['id'] === $id_prod) {
                $productoExiste = true;
                break;
            }
        }
        if ($productoExiste){
            return redirect()->back()->withInput()->with('cart_errors', 'El producto ya está en el carrito');
        }
        else{
            $articuloModel=New ArticuloModel();
            $articulo=$articuloModel->get_by_id($id_prod);
            if (count($articulo)>=0){
                 $this->cart->insert([
                'id'      => $id_prod,
                'qty'     => 1,
                'price'   => $articulo->precio,
                'name'    => $articulo->nombre,
                'genre'=>$articulo->genero,
                'editorial'=>$articulo->editorial,
                'author'=>$articulo->autor
                ]);
                $this->show_cart();
            }
           
        }
            
    }
}