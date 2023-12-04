#include<iostream>
#include<fstream>
#include<stdlib.h>
#include<time.h>
#include<direct.h>
#include<string>
#include<random>

using namespace std;
string calcularIdentificadorProducto(string categoria, int indice){
    string indiceEnString = to_string(indice+1);
    int tam = indiceEnString.size();
    int cerosFaltantes = 5 - tam;
    cout<<categoria<<endl;
    cout<<indice<<endl;
    indiceEnString = to_string(indice+1);
    string ceros="";
    for(int i = 0; i<cerosFaltantes;i++){
        ceros = ceros+'0';
    }
    char primero = categoria.at(0);
    char segundo = categoria.at(1);
    char tercero = categoria.at(2);
    string inicio = "xxx-";
    inicio.at(0) = primero;
    inicio.at(1) = segundo;
    inicio.at(2) = tercero;
    string identificador = inicio+ceros+indiceEnString;
    cout<<identificador<<endl;
    return identificador;
}
string calcularIdentificadorProveedor(int id){
    string idEnString = to_string(id);
    int tam = idEnString.size();
    int cerosFaltantes = 4 - tam;
    string ceros="";
    for(int i = 0; i<cerosFaltantes;i++){
        ceros = ceros+'0';
    }
    string identificador = "P"+ceros+idEnString;
    return identificador;
}
string calcularIdentificadorBoleta(int id,int dia, string mes, int anio){
    string idEnString = to_string(id);
    int tam = idEnString.size();
    int cerosFaltantes = 4 - tam;
    string ceros="";
    for(int i = 0; i<cerosFaltantes;i++){
        ceros = ceros+'0';
    }
    string identificador = "B"+ceros+idEnString+"-"+to_string(dia)+"-"+mes+"-"+to_string(anio);
    return identificador;
}
void rellenarPrecios(int* vector, int tam){
    for(int i = 0; i < tam; i++){
        vector[i] = 1+rand()%(51-1);
    }
}
string crearCarpeta(string nombre){
    string carpeta = "./"+nombre;
    mkdir(carpeta.c_str());
    return carpeta;
}
void crearCarpetaAnio(string nombre, int anio){
    string carpeta = "./"+nombre+"/"+to_string(anio);
    mkdir(carpeta.c_str());
}
string crearCarpetaMes(string nombre, string mes, int anio){
    string carpeta = "./"+nombre+"/"+to_string(anio)+"/"+mes;
    mkdir(carpeta.c_str());
    return carpeta;
}
void cambiarPreciosCompra(int* vector, int tam){
    int cantACambiar = 1+rand()%(6-1);
    for(int i = 0; i < cantACambiar; i++){
        int indice = 1+rand()%(tam-1);
        int nuevoPrecio = 1+rand()%(3-1);
        vector[indice] = vector[indice] + nuevoPrecio;
    }
}
int calcularPrecioVenta(int* vector, int indice){
    int precioVenta = vector[indice]*1.3;
    return precioVenta;
}
void crearArchivoCostos(int anio, string mes, int* vector, int tam, string categoria, string carpeta){
    ofstream archivo(carpeta+"/precios"+categoria+".csv");
    if(!archivo){
        cout<<"Error al crear el archivo"<<endl;
    }else{
        string identificador;
        int precio;
        archivo<<"Identificador,Precio"<<endl;
        for(int i = 0; i < tam; i++){
            identificador = calcularIdentificadorProducto(categoria, i);
            precio = vector[i];
            archivo<<identificador<<","<<to_string(precio)<<endl;
        }
        archivo.close();
    }
}
void crearArchivoFacturas(int dia, int anio, string mes, string carpeta, int* costos[], int* stock[], int* cantidadCategoria, string* nombreCategorias){
    ofstream archivo(carpeta+"/facturas"+to_string(dia)+"-"+mes+"-"+to_string(anio)+".csv");
    if(!archivo){
        cout<<"Error al crear el archivo"<<endl;
    }else{
        archivo<<"Proveedor,Producto,Cantidad,Precio Unitario,Precio Total"<<endl;
        string identificadorProveedor;
        string identificadorProducto;
        int cantidad;
        int precioUnitario;
        int precioTotal;
        for(int i = 1; i<=999; i++){
            int probabilidad = 1+rand()%(100-1);
            if(probabilidad>90){
                identificadorProveedor = calcularIdentificadorProveedor(i);
                int numeroCategoria = i%14;
                string nombreCategoria = nombreCategorias[numeroCategoria];
                int tamano = cantidadCategoria[numeroCategoria];
                int* listaCostos = costos[numeroCategoria];
                int* listaStock = stock[numeroCategoria];
                for(int j = 0; j<tamano; j++){
                    probabilidad = 1+rand()%(100-1);
                    if(probabilidad>90){
                        identificadorProducto = calcularIdentificadorProducto(nombreCategoria, j);
                        cantidad = 1+rand()%(10-1);
                        precioUnitario = listaCostos[j];
                        precioTotal = precioUnitario*cantidad;
                        listaStock[j] = listaStock[j] + cantidad;
                        archivo<<identificadorProveedor<<","<<identificadorProducto<<","<<to_string(cantidad)<<","<<to_string(precioUnitario)<<","<<to_string(precioTotal)<<endl;
                    }
                }
            }
        }
        archivo.close();
    }
}
void crearArchivoStock(int dia, int anio, string mes, int* vector, int tam, string categoria, string carpeta){
    ofstream archivo(carpeta+"/inventario"+categoria+to_string(dia)+"-"+mes+"-"+to_string(anio)+".csv");
    if(!archivo){
        cout<<"Error al crear el archivo"<<endl;
    }else{
        string identificador;
        int cantidad;
        archivo<<"Identificador,Cantidad"<<endl;
        for(int i = 0; i < tam; i++){
            identificador = calcularIdentificadorProducto(categoria, i);
            cantidad = vector[i];
            archivo<<identificador<<","<<to_string(cantidad)<<endl;
        }
        archivo.close();
    }
}
void crearArchivoBoletas(int dia, int anio, string mes, string carpeta, int* costos[], int* stock[], int* cantidadCategoria, string* nombreCategorias){
    ofstream archivo(carpeta+"/boletas"+to_string(dia)+"-"+mes+"-"+to_string(anio)+".csv");
    int cantidadVentas = 250+rand()%(501-1);
    if(!archivo){
        cout<<"Error al crear el archivo"<<endl;
    }else{
        archivo<<"Boleta,Productos,Precio Total"<<endl;
        for(int h = 1; h<= cantidadVentas; h++){
            int cantidadProductos = 1+rand()%(31-1);
            int precioFinal = 0;
            string identificadorBoleta;
            string listaProductos = "";
            for(int i=0;i<cantidadProductos;i++){
                int numeroCategoria = 1+rand()%(14-1);
                string nombreCategoria = nombreCategorias[numeroCategoria];
                int tamano = cantidadCategoria[numeroCategoria];
                int productoEspecifico = 1+rand()%((tamano+1)-1);
                int* listaStock = stock[numeroCategoria];
                if(listaStock[productoEspecifico] > 0){
                    listaProductos = listaProductos+"," + calcularIdentificadorProducto(nombreCategoria,productoEspecifico);
                    int* listaCostos = costos[numeroCategoria];
                    precioFinal = precioFinal + calcularPrecioVenta(listaCostos, productoEspecifico);
                    listaStock[productoEspecifico] = listaStock[productoEspecifico] - 1;
                }
            }
            identificadorBoleta = calcularIdentificadorBoleta(h, dia, mes, anio);
            archivo<<identificadorBoleta<<listaProductos<<","<<to_string(precioFinal)<<endl;
        }
        archivo.close();
    }
}
int main(){
    srand( time(NULL) );
    int cantProveedores = 999;
    int cantidadesProducto [14]= {156, 234, 260, 130, 208, 78, 156, 338, 182, 182, 156, 130, 130, 130};
    string nombreCategorias[14] = {"Bebes", "Belleza", "Congelados", "Deportes", "Desayuno", "Electro", "Farmacia", "Hogar", "Jugueteria", "Libreria", "Licores", "Panaderia", "Pescaderia", "Quesos"};
    string meses[12] = {"Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"};
    int dias[12] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    int anioInicio = 2005;
    int* vectoresPrecios[14];
    int* vectoresStock[14];
    int* preciosBebe = new int[cantidadesProducto[0]];
    int* preciosBelleza = new int[cantidadesProducto[1]];
    int* preciosCongelados = new int[cantidadesProducto[2]];
    int* preciosDeportes = new int[cantidadesProducto[3]];
    int* preciosDesayuno = new int[cantidadesProducto[4]];
    int* preciosElectro = new int[cantidadesProducto[5]];
    int* preciosFarmacia = new int[cantidadesProducto[6]];
    int* preciosHogar = new int[cantidadesProducto[7]];
    int* preciosJugueteria = new int[cantidadesProducto[8]];
    int* preciosLibreria = new int[cantidadesProducto[9]];
    int* preciosLicores = new int[cantidadesProducto[10]];
    int* preciosPanaderia = new int[cantidadesProducto[11]];
    int* preciosPescaderia = new int[cantidadesProducto[12]];
    int* preciosQuesos = new int[cantidadesProducto[13]];
    int* stockBebe = new int[cantidadesProducto[0]];
    int* stockBelleza = new int[cantidadesProducto[1]];
    int* stockCongelados = new int[cantidadesProducto[2]];
    int* stockDeportes = new int[cantidadesProducto[3]];
    int* stockDesayuno = new int[cantidadesProducto[4]];
    int* stockElectro = new int[cantidadesProducto[5]];
    int* stockFarmacia = new int[cantidadesProducto[6]];
    int* stockHogar = new int[cantidadesProducto[7]];
    int* stockJugueteria = new int[cantidadesProducto[8]];
    int* stockLibreria = new int[cantidadesProducto[9]];
    int* stockLicores = new int[cantidadesProducto[10]];
    int* stockPanaderia = new int[cantidadesProducto[11]];
    int* stockPescaderia = new int[cantidadesProducto[12]];
    int* stockQuesos = new int[cantidadesProducto[13]];
    vectoresPrecios[0] = preciosBebe;
    vectoresPrecios[1] = preciosBelleza;
    vectoresPrecios[2] = preciosCongelados;
    vectoresPrecios[3] = preciosDeportes;
    vectoresPrecios[4] = preciosDesayuno;
    vectoresPrecios[5] = preciosElectro;
    vectoresPrecios[6] = preciosFarmacia;
    vectoresPrecios[7] = preciosHogar;
    vectoresPrecios[8] = preciosJugueteria;
    vectoresPrecios[9] = preciosLibreria;
    vectoresPrecios[10] = preciosLicores;
    vectoresPrecios[11] = preciosPanaderia;
    vectoresPrecios[12] = preciosPescaderia;
    vectoresPrecios[13] = preciosQuesos;
    vectoresStock[0] = stockBebe;
    vectoresStock[1] = stockBelleza;
    vectoresStock[2] = stockCongelados;
    vectoresStock[3] = stockDeportes;
    vectoresStock[4] = stockDesayuno;
    vectoresStock[5] = stockElectro;
    vectoresStock[6] = stockFarmacia;
    vectoresStock[7] = stockHogar;
    vectoresStock[8] = stockJugueteria;
    vectoresStock[9] = stockLibreria;
    vectoresStock[10] = stockLicores;
    vectoresStock[11] = stockPanaderia;
    vectoresStock[12] = stockPescaderia;
    vectoresStock[13] = stockQuesos;
    string carpetas [] = {"Facturas","Inventario","Precios","Boletas"};
    for (int i = 0; i < 14; i++)
    {
        rellenarPrecios(vectoresPrecios[i], cantidadesProducto[i]);
    }
    for (int i = 0; i < 4; i++)
    {
        crearCarpeta(carpetas[i]);
    }
    for(int i = anioInicio; i <= 2022; i++){
        crearCarpetaAnio(carpetas[0], i);
        crearCarpetaAnio(carpetas[1], i);
        crearCarpetaAnio(carpetas[2], i);
        crearCarpetaAnio(carpetas[3], i);
        for(int j = 0; j < 12; j++){
            string carpetaFacturas = crearCarpetaMes(carpetas[0], meses[j],i);
            string carpetaInventario = crearCarpetaMes(carpetas[1], meses[j],i);
            string carpetaPrecios = crearCarpetaMes(carpetas[2], meses[j],i);
            string carpetaBoletas = crearCarpetaMes(carpetas[3], meses[j],i);
            for(int k = 0; k<14; k++){
                crearArchivoCostos(i, meses[j], vectoresPrecios[k], cantidadesProducto[k], nombreCategorias[k], carpetaPrecios);
            }
            for(int k = 1; k<=dias[j]; k++){
                crearArchivoFacturas(k,i,meses[j],carpetaFacturas, vectoresPrecios, vectoresStock, cantidadesProducto, nombreCategorias);
                for(int z = 0; z<14; z++){
                    crearArchivoStock(k,i,meses[j],vectoresStock[z],cantidadesProducto[z], nombreCategorias[z], carpetaInventario);
                }
                crearArchivoBoletas(k,i,meses[j],carpetaBoletas, vectoresPrecios, vectoresStock, cantidadesProducto, nombreCategorias);
            }
            for(int k = 0; k<14; k++){
                cambiarPreciosCompra(vectoresPrecios[k],cantidadesProducto[k]);
            }
        }
    }
    return 0;
}