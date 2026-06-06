from tiny_reflex.queries.VentasKPIQueries import obtener_categorias

def main():
    datos = obtener_categorias()
    print(datos)
  

if __name__ == "__main__":
    main()