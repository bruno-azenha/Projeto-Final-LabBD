/*
LAB BD - Turma B

Nomes:

Anayã Gimenes Ferreira 8066457
Bruno Azenha Gonçalves 7143444
Guilherme Augusto Bileki 4287189

*/



CREATE TABLE cliente (
  codigo number,
  tratamento varchar2 (8),
  primeironome varchar2 (50) NOT NULL,
  nomedomeio varchar2 (50),
  sobrenome varchar2 (50) NOT NULL,
  sufixo varchar2 (10),
  senha varchar2 (128) NOT NULL
);

CREATE TABLE endereco (
  id number,
  logradouro varchar2 (60) NOT NULL,
  complemento varchar2 (60),
  cidade varchar2 (30) NOT NULL,
  estado varchar2 (50) NOT NULL,
  pais varchar2 (50) NOT NULL,
  codigopostal varchar2 (15) NOT NULL
);

CREATE TABLE clienteendereco (
  codigocliente number,
  idendereco number,
  tipoendereco varchar2 (50)
);

CREATE TABLE modelo (
  codigo number,
  nome varchar2 (50) NOT NULL
);

CREATE TABLE categoria (
  codigo number,
  nome varchar2 (50) NOT NULL,
  categoriaprincipal number
);

CREATE TABLE produto (
  codigo varchar2 (15),
  nome varchar2 (50) NOT NULL,
  cor varchar2 (15),
  custoproducao number NOT NULL,
  preco number NOT NULL,
  tamanho varchar2 (5),
  peso number,
  codigomodelo number,
  codigocategoria number,
  dtiniciovenda timestamp,
  dtfimvenda timestamp
);

CREATE TABLE vendedor (
  codigo number,
  primeironome varchar2 (50) NOT NULL,
  nomedomeio varchar2 (50),
  sobrenome varchar2 (50) NOT NULL,
  senha varchar2 (128) NOT NULL,
  dtnascimento timestamp NOT NULL,
  dtcontratacao timestamp NOT NULL,
  sexo varchar2 (1),
  quota number,
  bonus number,
  comissao number
);

CREATE TABLE transportadora (
    codigo number,
    nome varchar2(50) NOT NULL,
    taxabase number NOT NULL,
    taxaenvio number NOT NULL
);

CREATE TABLE idioma (
  sigla varchar2 (6),
  nome varchar2 (50) NOT NULL
);

CREATE TABLE descricao (
  codigo number,
  descricao varchar2 (650),
  codigomodelo number,
  siglaidioma varchar2 (6)
);

CREATE TABLE pedido (
  codigo number,
  dtpedido timestamp NOT NULL,
  dtenvio timestamp,
  dtrecebimento timestamp,
  codigocliente number NOT NULL,
  contacliente varchar2 (15),
  numerocartaocredito number,
  codigoconfirmacao varchar2 (15),
  codigovendedor number,
  imposto number,
  enderecofatura number,
  enderecoentrega number,
  codigotransportadora number
);

CREATE TABLE detalhespedido (
  codigopedido number,
  codigoproduto varchar2 (15),
  quantidade number NOT NULL,
  precounitario number NOT NULL,
  desconto number
);

ALTER TABLE Cliente ADD PRIMARY KEY(codigo);
ALTER TABLE Endereco ADD PRIMARY KEY(id);
ALTER TABLE Modelo ADD PRIMARY KEY(codigo);
ALTER TABLE Categoria ADD PRIMARY KEY(codigo);
ALTER TABLE Produto ADD PRIMARY KEY(codigo);
ALTER TABLE Vendedor ADD PRIMARY KEY(codigo);
ALTER TABLE Transportadora ADD PRIMARY KEY(codigo);
ALTER TABLE Idioma ADD PRIMARY KEY(sigla);
ALTER TABLE Descricao ADD PRIMARY KEY(codigo);
ALTER TABLE Pedido ADD PRIMARY KEY(codigo);
ALTER TABLE ClienteEndereco ADD PRIMARY KEY(codigocliente, idendereco);
ALTER TABLE DetalhesPedido ADD PRIMARY KEY(codigopedido, codigoproduto);

ALTER TABLE ClienteEndereco ADD CONSTRAINT FK_clienteEndereco_cliente FOREIGN KEY (codigocliente) REFERENCES Cliente(codigo);
ALTER TABLE ClienteEndereco ADD CONSTRAINT FK_clienteEndereco_endereco FOREIGN KEY (idendereco) REFERENCES Endereco(id);
ALTER TABLE Categoria ADD CONSTRAINT FK_categoria_categoria FOREIGN KEY (categoriaprincipal) REFERENCES Categoria(codigo);
ALTER TABLE Produto ADD CONSTRAINT FK_produto_modelo FOREIGN KEY (codigomodelo) REFERENCES Modelo(codigo);
ALTER TABLE Produto ADD CONSTRAINT FK_produto_categoria FOREIGN KEY (codigocategoria) REFERENCES Categoria(codigo);
ALTER TABLE Descricao ADD CONSTRAINT FK_descricao_modelo FOREIGN KEY (codigomodelo) REFERENCES Modelo(codigo);
ALTER TABLE Descricao ADD CONSTRAINT FK_descricao_idioma FOREIGN KEY (siglaidioma) REFERENCES Idioma(sigla);
ALTER TABLE Pedido ADD CONSTRAINT FK_pedido_cliente FOREIGN KEY (codigocliente) REFERENCES Cliente(codigo);
ALTER TABLE Pedido ADD CONSTRAINT FK_pedido_vendedor FOREIGN KEY (codigovendedor) REFERENCES Vendedor(codigo);
ALTER TABLE Pedido ADD CONSTRAINT FK_pedido_enderecoFatura FOREIGN KEY (enderecofatura) REFERENCES Endereco(id);
ALTER TABLE Pedido ADD CONSTRAINT FK_pedido_enderecoEntrega FOREIGN KEY (enderecoentrega) REFERENCES Endereco(id);
ALTER TABLE Pedido ADD CONSTRAINT FK_pedido_transportadora FOREIGN KEY (codigotransportadora) REFERENCES Transportadora(codigo);
ALTER TABLE DetalhesPedido ADD CONSTRAINT FK_detalhesPedido_pedido FOREIGN KEY (codigopedido) REFERENCES Pedido(codigo);
ALTER TABLE DetalhesPedido ADD CONSTRAINT FK_detalhesPedido_produto FOREIGN KEY (codigoproduto) REFERENCES Produto(codigo);