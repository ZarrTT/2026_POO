from datetime import datetime
import json

class Cliente:
    def __init__(self, id, n, e, f):
        self.setId(id)
        self.setNome(n)
        self.setEmail(e)
        self.setFone(f)

    def ToString(self):
        return f'Cliente N°{self.__id}, Nome: {self.__nome}, E-mail: {self.__email}, Telefone: {self.__fone}'
    
    def setId(self, id):
        if id > 0:
            self.__id = id
        else: raise ValueError("Seu ID é Invalido!")

    def setNome(self, n):
        if n != "":
            self.__nome = n
        else: raise ValueError("Seu Nome está vazio!")

    def setEmail(self, e):
        if e != "":
            self.__email = e
        else: raise ValueError("Seu Email está vazio!")

    def setFone(self, f):
        if f != "":
            self.__fone = f
        else: raise ValueError("Seu Telefone está vazio!")

    def getID(self):
        return self.__id
    
    def getNome(self):
        return self.__nome
    
    def getEmail(self):
        return self.__email
    
    def getFone(self):
        return self.__fone


class Categoria:
    def __init__(self, id, d):
        self.setId(id)
        self.setD(d)

    def ToString(self):
        return f'ID N°: {self.__id} Descrição: {self.__d}!'
    
    def setId(self, id):
        if id > 0 :
            self.__id = id
        else: raise ValueError("Seu ID é inválido!")

    def setD(self, d):
        if d != "":
            self.__d = d
        else: raise ValueError("Descrição Inválida!")

    def getId(self):
        return self.__id
    
    def getD(self):
        return self.__d
    
class Produto:
    def __init__(self, id, d, p, e, id_cat):
        self.setID(id)
        self.setD(d)
        self.setP(p)
        self.setE(e)
        self.setIdCat(id_cat)

    def ToString(self):
        return f'Produto N° {self.__id}, Descrição: {self.__d}, Preço: {self.__p}, Estoque: {self.__e}, ID Categoria: {self.__idCat}'
    
    def setID(self, id):
        if id > 0:
            self.__id = id
        else: raise ValueError("ID Inválido")
    
    def setD(self, d):
        if d != "":
            self.__d = d
        else: raise ValueError("Descrição Inválida")

    def setP(self, p):
        if p >= 0:
            self.__p = p
        else: raise ValueError("Preço Inválido!")
    
    def setE(self, e):
        if e >= 0:
            self.__e = e
        else: raise ValueError("Estoque Inválido!")
    
    def setIdCat(self, idCat):
        if idCat > 0:
            self.__idCat = idCat
        else: raise ValueError("Id de Categoria Inválido!")
    
    def getID(self):
        return self.__id
    
    def getD(self):
        return self.__d
    
    def getP(self):
        return self.__p
    
    def getE(self):
        return self.__e
    
    def getIdCat(self):
        return self.__idCat
    
class Venda:
    def __init__(self, id):
        self.setID(id) 
        self.__data = None
        self.__carrinho = False
        self.__total = 0.0
        self.__idCliente = 0
    
    def ToString(self):

        return f'Venda N° {self.__id}, Data: {self.__data}, Carrinho: {self.__carrinho}, Total: R${self.__total}, ID Cliente: {self.__idCliente}'
    

    def setID(self, id):
        if id > 0:
            self.__id = id
        else: raise ValueError("ID Inválido")
    
    def setData(self, data):
        if isinstance(data, datetime):
            self.__data = data
        else: raise ValueError("Data inválida!")

    def setCarrinho(self, c):
        if isinstance(c, bool):
            self.__carrinho = c
        else: raise ValueError("Status do carrinho inválido!")

    def setTotal(self, t):
        if t >= 0:
            self.__total = t
        else: raise ValueError("O total não pode ser negativo!")

    def setIdCliente(self, id_cliente):
        if id_cliente > 0:
            self.__idCliente = id_cliente
        else: raise ValueError("ID do Cliente Inválido!")

    def getID(self):
        return self.__id
    
    def getData(self):
        return self.__data
    
    def getCarrinho(self):
        return self.__carrinho
    
    def getTotal(self):
        return self.__total
    
    def getIdCliente(self):
        return self.__idCliente

class VendaItem:
    def __init__(self, id, q, p):
        self.setID(id)
        self.setQtd(q)
        self.setPreco(p)
        self.__idVenda = 0
        self.__idProduto = 0

    def ToString(self):
        return f'Item N° {self.__id} | Qtd: {self.__qtd} | Preço: R${self.__preco} | Venda ID: {self.__idVenda} | Produto ID: {self.__idProduto}'

    def setID(self, id):
        if id > 0:
            self.__id = id
        else: raise ValueError("ID Inválido")

    def setQtd(self, q):
        if q > 0:
            self.__qtd = q
        else: raise ValueError("Quantidade Inválida")

    def setPreco(self, p):
        if p >= 0:
            self.__preco = p
        else: raise ValueError("Preço Inválido")

    def setIdVenda(self, idVenda):
        if idVenda > 0:
            self.__idVenda = idVenda
        else: raise ValueError("ID da Venda Inválido")

    def setIdProduto(self, idProduto):
        if idProduto > 0:
            self.__idProduto = idProduto
        else: raise ValueError("ID do Produto Inválido")

    def getID(self):
        return self.__id

    def getQtd(self):
        return self.__qtd

    def getPreco(self):
        return self.__preco

    def getIdVenda(self):
        return self.__idVenda

    def getIdProduto(self):
        return self.__idProduto


class ClienteDAO:
    objetos = []

    @classmethod
    def Inserir(cls, obj):
        cls.objetos.append(obj)

    @classmethod
    def Listar(cls):
        return cls.objetos

    @classmethod
    def Listar_id(cls, id):
        for obj in cls.objetos:
            if obj.getID() == id:
                return obj
        return None

    @classmethod
    def Atualizar(cls, obj):
        cliente = cls.Listar_id(obj.getID())
        if cliente:
            cliente.setNome(obj.getNome())
            cliente.setEmail(obj.getEmail())
            cliente.setFone(obj.getFone())

    @classmethod
    def Excluir(cls, obj):
        cliente = cls.Listar_id(obj.getID())
        if cliente:
            cls.objetos.remove(cliente)

    @classmethod
    def Salvar(cls):
        with open('clientes.json', 'w') as f:
            lista_dicts = []
            for obj in cls.objetos:
                lista_dicts.append({
                    'id': obj.getID(),
                    'nome': obj.getNome(),
                    'email': obj.getEmail(),
                    'fone': obj.getFone()
                })
            json.dump(lista_dicts, f, indent=4)

    @classmethod
    def Abrir(cls):
        cls.objetos = []
        try:
            with open('clientes.json', 'r') as f:
                lista_dicts = json.load(f)
                for d in lista_dicts:
                    cliente = Cliente(d['id'], d['nome'], d['email'], d['fone'])
                    cls.objetos.append(cliente)
        except FileNotFoundError:
            pass

class CategoriaDAO:
    objetos = []

    @classmethod
    def Inserir(cls, obj): 
        cls.objetos.append(obj)

    @classmethod
    def Listar(cls): 
        return cls.objetos

    @classmethod
    def Listar_id(cls, id):
        for obj in cls.objetos:
            if obj.getId() == id: return obj
        return None

    @classmethod
    def Atualizar(cls, obj):
        categoria = cls.Listar_id(obj.getId())
        if categoria:
            categoria.setD(obj.getD())

    @classmethod
    def Excluir(cls, obj):
        categoria = cls.Listar_id(obj.getId())
        if categoria: cls.objetos.remove(categoria)

    @classmethod
    def Salvar(cls):
        with open('categorias.json', 'w') as f:
            lista_dicts = [{'id': obj.getId(), 'd': obj.getD()} for obj in cls.objetos]
            json.dump(lista_dicts, f, indent=4)

    @classmethod
    def Abrir(cls):
        cls.objetos = []
        try:
            with open('categorias.json', 'r') as f:
                lista_dicts = json.load(f)
                for d in lista_dicts:
                    categoria = Categoria(d['id'], d['d'])
                    cls.objetos.append(categoria)
        except FileNotFoundError: pass

class ProdutoDAO:
    objetos = []

    @classmethod
    def Inserir(cls, obj): 
        cls.objetos.append(obj)

    @classmethod
    def Listar(cls): 
        return cls.objetos

    @classmethod
    def Listar_id(cls, id):
        for obj in cls.objetos:
            if obj.getID() == id: return obj
        return None

    @classmethod
    def Atualizar(cls, obj):
        produto = cls.Listar_id(obj.getID())
        if produto:
            produto.setD(obj.getD())
            produto.setP(obj.getP())
            produto.setE(obj.getE())
            produto.setIdCat(obj.getIdCat())

    @classmethod
    def Excluir(cls, obj):
        produto = cls.Listar_id(obj.getID())
        if produto: cls.objetos.remove(produto)

    @classmethod
    def Salvar(cls):
        with open('produtos.json', 'w') as f:
            lista_dicts = []
            for obj in cls.objetos:
                lista_dicts.append({
                    'id': obj.getID(), 'd': obj.getD(), 
                    'p': obj.getP(), 'e': obj.getE(), 'id_cat': obj.getIdCat()
                })
            json.dump(lista_dicts, f, indent=4)

    @classmethod
    def Abrir(cls):
        cls.objetos = []
        try:
            with open('produtos.json', 'r') as f:
                lista_dicts = json.load(f)
                for d in lista_dicts:
                    produto = Produto(d['id'], d['d'], d['p'], d['e'], d['id_cat'])
                    cls.objetos.append(produto)
        except FileNotFoundError: pass

class VendaDAO:
    objetos = []

    @classmethod
    def Inserir(cls, obj): 
        cls.objetos.append(obj)

    @classmethod
    def Listar(cls): 
        return cls.objetos

    @classmethod
    def Listar_id(cls, id):
        for obj in cls.objetos:
            if obj.getID() == id: return obj
        return None

    @classmethod
    def Atualizar(cls, obj):
        venda = cls.Listar_id(obj.getID())
        if venda:
            venda.setData(obj.getData())
            venda.setCarrinho(obj.getCarrinho())
            venda.setTotal(obj.getTotal())
            venda.setIdCliente(obj.getIdCliente())

    @classmethod
    def Excluir(cls, obj):
        venda = cls.Listar_id(obj.getID())
        if venda: cls.objetos.remove(venda)

    @classmethod
    def Salvar(cls):
        with open('vendas.json', 'w') as f:
            lista_dicts = []
            for obj in cls.objetos:
                data_texto = obj.getData().strftime('%Y-%m-%d %H:%M:%S') if obj.getData() else None
                lista_dicts.append({
                    'id': obj.getID(), 'data': data_texto,
                    'carrinho': obj.getCarrinho(), 'total': obj.getTotal(),
                    'idCliente': obj.getIdCliente()
                })
            json.dump(lista_dicts, f, indent=4)

    @classmethod
    def Abrir(cls):
        cls.objetos = []
        try:
            with open('vendas.json', 'r') as f:
                lista_dicts = json.load(f)
                for d in lista_dicts:
                    venda = Venda(d['id'])
                    if d['data']:
                        data_obj = datetime.strptime(d['data'], '%Y-%m-%d %H:%M:%S')
                        venda.setData(data_obj)
                    venda.setCarrinho(d['carrinho'])
                    venda.setTotal(d['total'])
                    venda.setIdCliente(d['idCliente'])
                    cls.objetos.append(venda)
        except FileNotFoundError: pass

class VendaItemDAO:
    objetos = []

    @classmethod
    def Inserir(cls, obj): 
        cls.objetos.append(obj)

    @classmethod
    def Listar(cls): 
        return cls.objetos

    @classmethod
    def Listar_id(cls, id):
        for obj in cls.objetos:
            if obj.getID() == id: return obj
        return None

    @classmethod
    def Atualizar(cls, obj):
        item = cls.Listar_id(obj.getID())
        if item:
            item.setQtd(obj.getQtd())
            item.setPreco(obj.getPreco())
            item.setIdVenda(obj.getIdVenda())
            item.setIdProduto(obj.getIdProduto())

    @classmethod
    def Excluir(cls, obj):
        item = cls.Listar_id(obj.getID())
        if item: cls.objetos.remove(item)

    @classmethod
    def Salvar(cls):
        with open('venda_itens.json', 'w') as f:
            lista_dicts = []
            for obj in cls.objetos:
                lista_dicts.append({
                    'id': obj.getID(), 'qtd': obj.getQtd(),
                    'preco': obj.getPreco(), 'idVenda': obj.getIdVenda(),
                    'idProduto': obj.getIdProduto()
                })
            json.dump(lista_dicts, f, indent=4)

    @classmethod
    def Abrir(cls):
        cls.objetos = []
        try:
            with open('venda_itens.json', 'r') as f:
                lista_dicts = json.load(f)
                for d in lista_dicts:
                    item = VendaItem(d['id'], d['qtd'], d['preco'], d['idVenda'], d['idProduto'])
                    cls.objetos.append(item)
        except FileNotFoundError: pass

class UI:
    @classmethod
    def Main(cls):
        ClienteDAO.Abrir()
        CategoriaDAO.Abrir()
        ProdutoDAO.Abrir()
        
        op = -1
        while op != 0:
            op = cls.Menu()
            if op == 1: cls.Cliente_Inserir()
            elif op == 2: cls.Cliente_Listar()
            elif op == 3: cls.Cliente_Atualizar()
            elif op == 4: cls.Cliente_Excluir()
            elif op == 5: cls.Categoria_Inserir()
            elif op == 6: cls.Categoria_Listar()
            elif op == 7: cls.Categoria_Atualizar()
            elif op == 8: cls.Categoria_Excluir()
            elif op == 9: cls.Produto_Inserir()
            elif op == 10: cls.Produto_Listar()
            elif op == 11: cls.Produto_Atualizar()
            elif op == 12: cls.Produto_Excluir()
            
        ClienteDAO.Salvar()
        CategoriaDAO.Salvar()
        ProdutoDAO.Salvar()

    @classmethod
    def Menu(cls):
        print("\n1 - Inserir Cliente")
        print("2 - Listar Clientes")
        print("3 - Atualizar Cliente")
        print("4 - Excluir Cliente")
        print("5 - Inserir Categoria")
        print("6 - Listar Categorias")
        print("7 - Atualizar Categoria")
        print("8 - Excluir Categoria")
        print("9 - Inserir Produto")
        print("10 - Listar Produtos")
        print("11 - Atualizar Produto")
        print("12 - Excluir Produto")
        print("0 - Sair")
        return int(input("Escolha uma opcao: "))

    @classmethod
    def Cliente_Inserir(cls):
        id = int(input("ID: "))
        n = input("Nome: ")
        e = input("Email: ")
        f = input("Fone: ")
        obj = Cliente(id, n, e, f)
        ClienteDAO.Inserir(obj)

    @classmethod
    def Cliente_Listar(cls):
        for obj in ClienteDAO.Listar():
            print(obj.ToString())

    @classmethod
    def Cliente_Atualizar(cls):
        id = int(input("ID a atualizar: "))
        n = input("Novo Nome: ")
        e = input("Novo Email: ")
        f = input("Novo Fone: ")
        obj = Cliente(id, n, e, f)
        ClienteDAO.Atualizar(obj)

    @classmethod
    def Cliente_Excluir(cls):
        id = int(input("ID a excluir: "))
        obj = Cliente(id, "-", "-", "-")
        ClienteDAO.Excluir(obj)

    @classmethod
    def Categoria_Inserir(cls):
        id = int(input("ID: "))
        d = input("Descricao: ")
        obj = Categoria(id, d)
        CategoriaDAO.Inserir(obj)

    @classmethod
    def Categoria_Listar(cls):
        for obj in CategoriaDAO.Listar():
            print(obj.ToString())

    @classmethod
    def Categoria_Atualizar(cls):
        id = int(input("ID a atualizar: "))
        d = input("Nova Descricao: ")
        obj = Categoria(id, d)
        CategoriaDAO.Atualizar(obj)

    @classmethod
    def Categoria_Excluir(cls):
        id = int(input("ID a excluir: "))
        obj = Categoria(id, "-")
        CategoriaDAO.Excluir(obj)

    @classmethod
    def Produto_Inserir(cls):
        id = int(input("ID: "))
        d = input("Descricao: ")
        p = float(input("Preco: "))
        e = int(input("Estoque: "))
        id_cat = int(input("ID Categoria: "))
        obj = Produto(id, d, p, e, id_cat)
        ProdutoDAO.Inserir(obj)

    @classmethod
    def Produto_Listar(cls):
        for obj in ProdutoDAO.Listar():
            print(obj.ToString())

    @classmethod
    def Produto_Atualizar(cls):
        id = int(input("ID a atualizar: "))
        d = input("Nova Descricao: ")
        p = float(input("Novo Preco: "))
        e = int(input("Novo Estoque: "))
        id_cat = int(input("Novo ID Categoria: "))
        obj = Produto(id, d, p, e, id_cat)
        ProdutoDAO.Atualizar(obj)

    @classmethod
    def Produto_Excluir(cls):
        id = int(input("ID a excluir: "))
        obj = Produto(id, "-", 0.0, 0, 1)
        ProdutoDAO.Excluir(obj)

if __name__ == "__main__":
    UI.Main()