-- Tabla Cliente
CREATE TABLE Cliente (
    ID SERIAL PRIMARY KEY,
    Nombre VARCHAR(100),
    Telefono VARCHAR(20),
    NIT VARCHAR(20),
    Gmail VARCHAR(100),
    Contrasena VARCHAR(255)
);

-- Tabla Cupon
CREATE TABLE Cupon (
    ID SERIAL PRIMARY KEY,
    Nombre VARCHAR(100),
    Descripcion TEXT,
    Monto NUMERIC(10,2),
    Fecha DATE
);

-- Tabla Cliente_Cupon (intermedia)
CREATE TABLE Cliente_Cupon (
    Cliente_ID INT REFERENCES Cliente(ID),
    Cupon_ID INT REFERENCES Cupon(ID),
    PRIMARY KEY (Cliente_ID, Cupon_ID)
);

-- Tabla Metodo de Pago
CREATE TABLE Metodo_Pago (
    ID SERIAL PRIMARY KEY,
    Nombre VARCHAR(100),
    Descripcion TEXT
);

-- Tabla Venta
CREATE TABLE Venta (
    ID SERIAL PRIMARY KEY,
    Fecha DATE,
    Importe_Total NUMERIC(10,2),
    Importe_Total_Desc NUMERIC(10,2),
    Estado VARCHAR(50),
    Cliente_ID INT REFERENCES Cliente(ID),
    Metodo_Pago_ID INT REFERENCES Metodo_Pago(ID)
);

-- Tabla Reseña
CREATE TABLE Resena (
    ID SERIAL PRIMARY KEY,
    Descripcion TEXT,
    Puntuacion INT,
    Cliente_ID INT REFERENCES Cliente(ID),
    Producto_ID INT
);

-- Tabla Categoria
CREATE TABLE Categoria (
    ID SERIAL PRIMARY KEY,
    Nombre VARCHAR(100)
);

-- Tabla Marca
CREATE TABLE Marca (
    ID SERIAL PRIMARY KEY,
    Nombre VARCHAR(100)
);

-- Tabla Producto
CREATE TABLE Producto (
    ID SERIAL PRIMARY KEY,
    Nombre VARCHAR(100),
    Stock INT,
    Stock_Minimo INT,
    Stock_Maximo INT,
    Precio NUMERIC(10,2),
    Descripcion TEXT,
    Garantia TEXT,
    Categoria_ID INT REFERENCES Categoria(ID),
    Marca_ID INT REFERENCES Marca(ID)
);

-- Relacion Resena - Producto (agregada ahora)
ALTER TABLE Resena ADD CONSTRAINT fk_producto_resena FOREIGN KEY (Producto_ID) REFERENCES Producto(ID);

-- Tabla Imagen_Producto
CREATE TABLE Imagen_Producto (
    ID SERIAL PRIMARY KEY,
    Image_url TEXT,
    Producto_ID INT REFERENCES Producto(ID)
);

-- Tabla Movimiento
CREATE TABLE Movimiento (
    ID SERIAL PRIMARY KEY,
    TipoMovimiento VARCHAR(50),
    Cantidad INT,
    Fecha DATE,
    Descripcion TEXT,
    Producto_ID INT REFERENCES Producto(ID),
    Usuario_Codigo INT
);

-- Tabla Usuario
CREATE TABLE Usuario (
    Codigo SERIAL PRIMARY KEY,
    Nombre VARCHAR(100),
    Contrasena VARCHAR(100),
    Telefono VARCHAR(20),
    Apellido VARCHAR(100),
    Gmail VARCHAR(100),
    Estado VARCHAR(50)
);

-- Relación Movimiento - Usuario
ALTER TABLE Movimiento ADD CONSTRAINT fk_usuario_mov FOREIGN KEY (Usuario_Codigo) REFERENCES Usuario(Codigo);

-- Tabla Carrito
CREATE TABLE Carrito (
    ID SERIAL PRIMARY KEY,
    Cantidad INT,
    Estado VARCHAR(50),
    Importe NUMERIC(10,2),
    Importe_Desc NUMERIC(10,2),
    Precio NUMERIC(10,2),
    Venta_ID INT REFERENCES Venta(ID),
    Producto_ID INT REFERENCES Producto(ID)
);

-- Tabla Bitacora
CREATE TABLE Bitacora (
    ID SERIAL PRIMARY KEY,
    Accion TEXT,
    Fecha DATE,
    Hora TIME,
    Descripcion TEXT,
    Usuario_Codigo INT REFERENCES Usuario(Codigo)
);

-- Tabla Rol
CREATE TABLE Rol (
    ID SERIAL PRIMARY KEY,
    Nombre VARCHAR(100),
    Descripcion TEXT
);

-- Tabla Permiso
CREATE TABLE Permiso (
    ID SERIAL PRIMARY KEY,
    Nombre VARCHAR(100),
    Descripcion TEXT
);

-- Tabla Rol_Permiso (intermedia)
CREATE TABLE Rol_Permiso (
    Rol_ID INT REFERENCES Rol(ID),
    Permiso_ID INT REFERENCES Permiso(ID),
    PRIMARY KEY (Rol_ID, Permiso_ID)
);

-- Relación Usuario - Rol
ALTER TABLE Usuario ADD COLUMN Rol_ID INT REFERENCES Rol(ID);