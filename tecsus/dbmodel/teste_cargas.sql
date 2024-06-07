create table if not exists clientes (
    id serial primary key,
    nome varchar(100),
    email varchar(100),
    data_registro date default current_date
);

DO
$$

declare
  
  numero_registros int := 10000;

  begin
    for i in 1..numero_registros loop
        insert into clientes (nome,email) values ('User' || i,
                                                  'user'||i||'@gmail.com');
    end loop;
  end 
$$;

--truncate table clientes

create table if not exists testes_energia (
    id serial primary key,
    col1 varchar(100),
    col2 varchar(100),
    col3 varchar(100),
    col4 varchar(100),
    col5 varchar(100),
    col6 varchar(100),
    col7 varchar(100),
    col8 varchar(100),
    col9 varchar(100),
    col10 varchar(100),
    col11 varchar(100),
    col12 varchar(100),
    col13 varchar(100),
    col14 varchar(100),
    col15 varchar(100),
    col16 varchar(100),
    col17 varchar(100),
    col18 varchar(100),
    col19 varchar(100),
    col20 varchar(100),
    col21 varchar(100),
    col22 varchar(100),
    col23 varchar(100),
    col24 varchar(100),
    col25 varchar(100),
    data_registro date default current_date
);

DO
$$

declare
  
  numero_registros int := 25000;

  begin
    for i in 1..numero_registros loop
        insert into testes_energia (col1,col2,col3,col4,col5,col6,col7,col8,col9 ,col10,col11,col12,col13,col14,col15,col16,col17,col18,col19,col20,col21,col22,col23,col24,col25) 
                      values (i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i);
    end loop;
  end 
$$;

--truncate table testes_energia