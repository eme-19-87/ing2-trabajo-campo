<?php

namespace App\Controllers;

use CodeIgniter\Controller;
use CodeIgniter\Database\BaseConnection;
use CodeIgniter\HTTP\ResponseInterface;
use App\Models\CompraModel;
use App\Controllers\CartController;

class CompraController extends Controller
{
    protected $cart;
    protected $db;
    private $compra;

    public function __construct()
    {
        //parent::__construct(); 
        $this->cart = new CartController(); // ci4shoppingcart
        $this->db = \Config\Database::connect();
        $this->compra=new CompraModel();
    }

    private function controlarCarritoVacio(){
        return $this->cart->getCart()<=0;
    }
    public function controlarCompra(){
        if($this->controlarCarritoVacio()){
            return $this->response->setJSON([
                'success' => false,
                'message' => "El carrito está vacío"
            ]);
        } else{
                // Supongamos que el usuario ya inició sesión 
            $dni = 32837262;
            $fecha = date('d-m-y');
            $total = $this->cart->getTotal();

            // Construir JSON con los datos del carrito
            $items = [];
            foreach ($this->cart->getCart() as $item) {
                $items[] = [
                    'id'     => intval($item['id']),
                    'qty'    => $item['qty'],
                    'precio' => floatval($item['price'])
                ];
            }
            // Convertir a JSON
            $jsonDetalles = json_encode($items);
           return $this->registrarCompra($dni,$fecha,$total,$jsonDetalles);
        }
    }

    /**
     * Registra la compra de los artículos en el carrito
     */
    private function registrarCompra($dni, $fecha, $total, $detalles)
    {
        
        //dd($jsonDetalles);
        // Llamar al procedimiento
       

        // Obtener los valores OUT
        $mensajeRow = $this->compra->realizarCompra($total,$fecha,$dni,$detalles);
        //dd($mensajeRow);
        if ($mensajeRow->codigo >0) {
            $this->cart->destruirCart(); // Vaciar carrito en caso de éxito
            return $this->response->setJSON([
                'success' => true,
                'message' => $mensajeRow->mensaje
            ]);
        } else {
            return $this->response->setJSON([
                'success' => false,
                'message' => $mensajeRow->mensaje
            ]);
        }
    }
}
