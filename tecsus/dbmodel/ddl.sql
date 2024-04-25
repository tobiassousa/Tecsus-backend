create table pro_energia(
    id_pro_energia number constraint pk_pro_energia primary key
   ,leitura_anterior date not null
   ,leitura_atual date not null
   ,demanda_faturada_kw number not null
   ,total number not null
   ,fornecedor varchar(100) not null
   ,num_instalacao number not null
   ,num_cliente number not null
   ,modalidade varchar(20) not null
   ,num_contrato number not null
   ,constraint fk_prct_energia foreign key(num_instalacao) references contrato_energia(num_instalacao)
);

create table contrato_energia(
    id_contrato_energia number constraint pk_cont_energia primary key
   ,fornecedor varchar(100) not null
   ,num_instalacao number not null unique
   ,num_medidor varchar(100) not null
   ,num_cliente number not null
   ,modalidade varchar(20) not null
   ,forma_pagto varchar(20) not null
   ,email varchar(100) not null
   ,cidade varchar(200) not null
);

create table pro_agua(
    id_pro_agua number constraint pk_pro_agua primary key
   ,leitura_anterior date not null
   ,leitura_atual date not null
   ,consumo_agua_m3 number not null
   ,consumo_esgoto_m3 number not null
   ,vlr_agua number(16,2) not null
   ,vlr_esgoto number(16,2) not null
   ,vlr_total number(16,2) not null
   ,num_instalacao number not null
   ,num_medidor varchar(100) not null
   ,num_cliente number not null
   ,cod_ligacao_rgi varchar(100) not null
   ,num_contrato number not null
   ,constraint fk_prct_agua foreign key (num_instalacao) references contrato_agua(num_instalacao)
);

create table contrato_agua(
    id_contrato_agua number constraint pk_cont_agua primary key
   ,fornecedor varchar(100) not null
   ,num_instalacao number not null unique
   ,num_medidor varchar(100) not null
   ,num_cliente number not null
   ,modalidade varchar(20) not null
   ,num_contrato number not null
   ,tipo_pagto varchar(20) not null
   ,email varchar(100) not null
   ,cidade varchar(200) not null
);