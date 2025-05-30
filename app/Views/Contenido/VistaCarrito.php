<?php if (count($cart)<=0){;?>
    <p class="display-1 p-5 bg-danger m-5">
        Aún no ha agregado productos al carrito.
    </p>
<?php }else {;?>

 <table class="table table-striped table-hover text-center mt-3">
                <thead class="table-dark ">
                    <tr>
                        <th>Título</th>
                        <th>Precio</th>
                        <th>Autor</th>
                        <th>Editorial</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($cart as $id => $item): ?>
                        <tr>
                            <td><?= esc($item['name']) ?></td>
                            <td>$<?= number_format($item['price'], 2) ?></td>
                           <td><?= $item['author'] ?></td>
                           <td><?= $item['editorial'] ?></td>
                            <td>
                                <a class="btn-eliminar btn btn-sm btn-danger"  data-id="<?= $item['id'] ?>">Eliminar</a>
                            </td>
                        </tr>
                    <?php endforeach; ?>
                </tbody>
                <tfoot>
                   
                  
                </tfoot>
            </table>
            
            <div class="d-flex justify-content-between mx-2">
                <a href="<?= base_url('tienda') ?>" class="btn btn-danger">Eliminar Carrito</a>
                <a href="<?= base_url('/') ?>" class="btn btn-secondary">Seguir Comprando</a>
                <a href="<?= base_url('checkout') ?>" class="btn btn-success">Pagar Ahora</a>
            </div>
<?php }?>



