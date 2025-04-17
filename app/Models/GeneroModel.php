<?php

namespace App\Models;

use CodeIgniter\Model;

class GeneroModel extends Model
{
    protected $table = 'genero';

    // Método para llamar al procedimiento
    public function obtenerGeneros()
    {
        $db = \Config\Database::connect();
        $query = $db->query("CALL digibook.ObtenerGeneros()");
        return $query->getResult(); // devuelve array de objetos
    }
}
