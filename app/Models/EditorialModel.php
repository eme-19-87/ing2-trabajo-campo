<?php

namespace App\Models;

use CodeIgniter\Model;

class EditorialModel extends Model
{
    protected $table = 'editorial';

    // Método para llamar al procedimiento
    public function obtenerEditoriales()
    {
        $db = \Config\Database::connect();
        $query = $db->query("CALL digibook.ObtenerEditorial()");
        return $query->getResult(); // devuelve array de objetos
    }
}
