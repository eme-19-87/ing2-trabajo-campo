<?php

use CodeIgniter\Router\RouteCollection;

/**
 * @var RouteCollection $routes
 */
$routes->get('/', 'Home::index',['as'=>'index']);
$routes->get('products', 'ArticuloController::show_product_form');
$routes->post('create_book', 'ArticuloController::validarDatos');








