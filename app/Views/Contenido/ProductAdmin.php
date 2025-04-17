<div class="container w-75">
<form class="m-3">
  <div class="mb-3">
    <label for="titulo_libro" class="form-label">Nombre</label>
    <input type="text" class="form-control" id="nombre_libro" name="titulo_libro" aria-describedby="emailHelp">
  </div>
  <div class="mb-3">
    <label for="precio_libro" class="form-label">Precio</label>
    <input type="text" class="form-control" id="precio_libro", name="precio_libro">
  </div>

  <div class="mb-3">
  <label for="genero_libro" class="form-label">Genero</label>
  <select name="genero_libro" name="genero_libro">
        <?php foreach ($generos as $g): ?>
            <option value="<?= esc($g->idGenero) ?>">
                <?= esc($g->nombre) ?>
            </option>
        <?php endforeach; ?>
    </select>
  </div>
  <div class="mb-3 form-check">
    <input type="checkbox" class="form-check-input" id="exampleCheck1">
    <label class="form-check-label" for="exampleCheck1">Check me out</label>
  </div>
  <button type="submit" class="btn btn-primary">Submit</button>
</form>
</div>