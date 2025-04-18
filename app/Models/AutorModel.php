<?php

namespace App\Models;

use CodeIgniter\Model;

class AutorModel extends Model
{
    protected $table = 'autor';

    // Método para llamar al procedimiento
    public function obtenerAutores()
    {
        $db = \Config\Database::connect();
        $query = $db->query("CALL digibook.ObtenerAutores()");
        return $query->getResult(); // devuelve array de objetos
    }
}