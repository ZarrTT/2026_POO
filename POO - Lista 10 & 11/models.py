# models.py

class EcommerceException(Exception): 
    pass

class EmailDuplicadoError(EcommerceException):
    def __init__(self, email):
        super().__init__(f"O e-mail '{email}' já está cadastrado no sistema.")

class ProdutoSemCategoriaError(EcommerceException):
    def __init__(self, nome_produto):
        super().__init__(f"Não é possível cadastrar '{nome_produto}' sem uma categoria definida.")

class ProdutoVendidoError(EcommerceException):
    def __init__(self, nome_produto):
        super().__init__(f"Proibido excluir! O produto '{nome_produto}' já possui vendas registradas.")

class PromocaoInvalidaError(EcommerceException):
    def __init__(self):
        super().__init__("O preço promocional deve ser menor que o preço original do produto.")