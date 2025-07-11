import json
from collections import namedtuple


# ---------- NamedTuple para uso adicional (opcional) ----------
MenuItemTuple = namedtuple('MenuItemTuple', ['nombre', 'precio', 'tipo', 'tamano', 'sabor'])

# ---------- Clase Base ----------
class Menu_item:
    def __init__(self, name: str, price: float):
        self.__name = name
        self.__price = price

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def set_name(self, name: str):
        self.__name = name

    def set_price(self, price: float):
        self.__price = price

# ---------- Subclases ----------
class Beverage(Menu_item):
    def __init__(self, name, price, tipo, size, flavor):
        super().__init__(name, price)
        self.__type = tipo
        self.__size = size
        self.__flavor = flavor

    def get_type(self): return self.__type
    def get_size(self): return self.__size
    def get_flavor(self): return self.__flavor

    def set_type(self, tipo): self.__type = tipo
    def set_size(self, size): self.__size = size
    def set_flavor(self, flavor): self.__flavor = flavor

class Appetizer(Menu_item):
    def __init__(self, name, price, tipo, size):
        super().__init__(name, price)
        self.__type = tipo
        self.__size = size

    def get_type(self): return self.__type
    def get_size(self): return self.__size
    def set_type(self, tipo): self.__type = tipo
    def set_size(self, size): self.__size = size

class Main_course(Menu_item):
    def __init__(self, name, price, tipo, size):
        super().__init__(name, price)
        self.__type = tipo
        self.__size = size

    def get_type(self): return self.__type
    def get_size(self): return self.__size
    def set_type(self, tipo): self.__type = tipo
    def set_size(self, size): self.__size = size

class Dessert(Menu_item):
    def __init__(self, name, price, tipo, size, flavor):
        super().__init__(name, price)
        self.__type = tipo
        self.__size = size
        self.__flavor = flavor

    def get_type(self): return self.__type
    def get_size(self): return self.__size
    def get_flavor(self): return self.__flavor
    def set_type(self, tipo): self.__type = tipo
    def set_size(self, size): self.__size = size
    def set_flavor(self, flavor): self.__flavor = flavor

# ---------- Cola FIFO manual ----------
class ColaFIFO:
    def __init__(self):
        self.items = []

    def encolar(self, item):
        self.items.append(item)

    def desencolar(self):
        if not self.esta_vacia():
            return self.items.pop(0)
        else:
            print("Cola vacía")
            return None

    def esta_vacia(self):
        return len(self.items) == 0

# ---------- Clase Restaurante ----------
class Restaurante:
    def __init__(self):
        self.ordenes = ColaFIFO()

    def agregar_orden(self, orden):
        self.ordenes.encolar(orden)

    def atender_orden(self):
        return self.ordenes.desencolar()

# ---------- Clase Order ----------
class Order:
    def __init__(self, numero, mesa):
        self.numero = numero
        self.mesa = mesa
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

    def descuento(self):
        total = 0
        bebidas = appetizers = platos = postres = 0

        for i in self.items:
            tipo = i.get_type()
            if tipo == "beverage":
                bebidas += 1
            elif tipo == "appetizer":
                appetizers += 1
            elif tipo == "main_course":
                platos += 1
            elif tipo == "dessert":
                postres += 1

        if bebidas >= 1 and appetizers >= 1 and platos >= 1 and postres >= 1:
            total += 5000
        if bebidas >= 3 and appetizers >= 3 and platos >= 3 and postres >= 3:
            total += 20000
        if bebidas >= 5:
            total += 10000
        for i in self.items:
            if i.get_name() == "Pizza":
                total += 10000
                break
        return total

    def calculate_total(self):
        subtotal = sum(item.get_price() for item in self.items)
        return subtotal - self.descuento()

    def __str__(self):
        return ', '.join(item.get_name() for item in self.items)

# ---------- Clases de Pago ----------
class Payment:
    def __init__(self, order):
        self.order = order

class Tarjeta(Payment):
    def __init__(self, order, numero, cvv):
        super().__init__(order)
        self.numero = numero
        self.cvv = cvv
        self.monto = order.calculate_total()

    def pagar(self):
        print(f"Pagando {self.monto} con tarjeta terminada en {self.numero[-4:]}")

class Efectivo(Payment):
    def __init__(self, order, monto_entregado):
        super().__init__(order)
        self.entregado = monto_entregado
        self.monto = order.calculate_total()

    def pagar(self):
        if self.entregado >= self.monto:
            cambio = self.entregado - self.monto
            print(f"Pago exitoso. Cambio: ${cambio}")
        else:
            print(f"Faltan ${self.monto - self.entregado} para completar el pago.")

# ---------- Clase Menu con JSON ----------
class Menu:
    def __init__(self, archivo="menu.json"):
        self.archivo = archivo
        self.items = {}
        self.cargar_menu()

    def cargar_menu(self):
        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                self.items = json.load(f)
        except FileNotFoundError:
            self.items = {}

    def guardar_menu(self):
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(self.items, f, ensure_ascii=False, indent=2)

    def agregar_item(self, nombre, datos):
        self.items[nombre] = datos
        self.guardar_menu()

    def actualizar_item(self, nombre, nuevos_datos):
        if nombre in self.items:
            self.items[nombre] = nuevos_datos
            self.guardar_menu()
        else:
            print("Item no encontrado")

    def eliminar_item(self, nombre):
        if nombre in self.items:
            del self.items[nombre]
            self.guardar_menu()

    def mostrar_menu(self):
        for nombre, datos in self.items.items():
            print(f"{nombre}: {datos}")

# ---------- Crear objeto desde JSON ----------
def crear_item_desde_json(nombre, datos):
    tipo = datos.get("tipo")
    precio = datos.get("precio")
    size = datos.get("tamano")
    sabor = datos.get("sabor", "")

    if tipo == "beverage":
        return Beverage(nombre, precio, tipo, size, sabor)
    elif tipo == "appetizer":
        return Appetizer(nombre, precio, tipo, size)
    elif tipo == "main_course":
        return Main_course(nombre, precio, tipo, size)
    elif tipo == "dessert":
        return Dessert(nombre, precio, tipo, size, sabor)
    else:
        print("Tipo no reconocido")
        return None

# ---------- Ejemplo de uso ----------
if __name__ == "__main__":
    menu = Menu("menu.json")
    menu.mostrar_menu()

    # Crear orden
    order = Order(1, mesa=5)
    order.add_item(crear_item_desde_json("Agua", menu.items["Agua"]))
    order.add_item(crear_item_desde_json("Pizza", menu.items["Pizza"]))
    order.add_item(crear_item_desde_json("Nachos", menu.items["Nachos"]))
    order.add_item(crear_item_desde_json("Helado", menu.items["Helado"]))

    print(f"\nOrden: {order}")
    print("Total con descuentos:", order.calculate_total())

    # Pago
    pago = Efectivo(order, monto_entregado=30000)
    pago.pagar()

    # Agregar orden al restaurante
    r = Restaurante()
    r.agregar_orden(order)
    print("\nOrden atendida:")
    print(r.atender_orden())
