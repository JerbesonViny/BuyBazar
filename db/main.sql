/* ÁREA DE CRIAÇÃO DAS TABELAS */

create table if not exists usuarios (
  id integer primary key autoincrement,
  nome varchar(60) not null,
  login_email varchar(60) not null,
  senha varchar(20) not null
);

create table if not exists telefones (
  id integer primary key autoincrement,
  prefixo varchar(4) not null,
  ddd varchar(4) not null,
  numero varchar(9) not null,
  usuario_id integer,

  foreign key (usuario_id) references usuarios (id)
);

create table if not exists emails (
  id integer primary key autoincrement,
  email varchar(60) not null,
  usuario_id integer,
  
  foreign key (usuario_id) references usuarios (id)
);

create table  if not exists enderecos (
  id integer primary key autoincrement,
  cep varchar(20) not null,
  rua varchar(60) not null,
  bairro varchar(60) not null,
  numero_casa integer not null
);

create table if not exists usuarios_tem_enderecos (
  id integer primary key autoincrement,
  usuario_id integer,
  endereco_id integer,

  foreign key (usuario_id) references usuarios (id),
  foreign key (endereco_id) references enderecos (id)
);

CREATE TABLE IF NOT EXISTS produtos (
  id integer primary key autoincrement,
  nome varchar(45) not null,
  preco float not null,
  situacao varchar(10) not null,
  descricao text not null,
  data_pub datetime not null 
);

CREATE TABLE IF NOT EXISTS pedidos (
  id integer primary key autoincrement,
  data_compra datetime,
  usuario_id integer,

  foreign key (usuario_id) references usuarios(id)
);

CREATE TABLE IF NOT EXISTS aquisicoes (
  id integer primary key autoincrement,
  pedido_id integer,
  produto_id integer,

  foreign key (pedido_id) references pedidos(id),
  foreign key (produto_id) references produtos(id)
);

