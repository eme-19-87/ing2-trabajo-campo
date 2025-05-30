<?php

use CodeIgniter\Router\RouteCollection;

/**
 * @var RouteCollection $routes
 */
$routes->get('/', 'Home::index',['as'=>'index']);
$routes->get('products', 'ArticuloController::show_product_form');
$routes->post('create_book', 'ArticuloController::validarDatos');
$routes->get('cart', 'CartController::showCart');
$routes->post('cart/add/(:num)', 'CartController::controlAgregar/$1');
$routes->get('cart/remove/(:any)', 'CartController::eliminarArticulo/$1');
$routes->get('cart/delete', 'CartController::vaciarCarrito');








