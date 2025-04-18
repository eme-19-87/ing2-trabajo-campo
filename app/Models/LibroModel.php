<?php

namespace App\Models;

use CodeIgniter\Model;

class LibroModel extends Model
{
    public function create_book($data): bool
    {
        $db = \Config\Database::connect();

	//En este punto prepara la función, pero aún no la ejecuta
	//la forma de crear esta consulta es útil para evitar las inyecciones
        $builder = $db->prepare(static function ($db) {
            return $db->query("CALL createNewBook(?, ?, ?, ?, ?, ?, ?, ?, @resultado)");
        });
        //dd($data);
        

        // Ejecutar el procedimiento
        $builder->execute([
            $data['titulo'],
            $data['precio'],
            $data['editorial_id'],
            $data['sinopsis'],
            $data['paginas'],
            $data['autor_id'],
            $data['genero_id'],
            date($data['fecha_publicacion'])
        ]);

        // Consultar el resultado devuelto
	//Recordar que la función en MySQL retorna 1 en caso de ser todo correcto
	//y 0 en caso de que haya existido algún error.
        $query = $db->query("SELECT @resultado AS resultado");
        $row = $query->getRow();

        return ($row && $row->resultado == 1);
    }
}