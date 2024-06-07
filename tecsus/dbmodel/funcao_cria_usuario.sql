create or replace function cria_usuario(
  role_usuario int, -- 1 para admin, 2 para editor, 3 para leitor
  nom_usuario text,
  senha text,
  nome_db text,
  nome_schema text
  ) returns void as

$$

begin
  --Criação do usuário
  execute format('CREATE USER %I WITH PASSWORD %L',nom_usuario,senha);

  --Acesso ao banco
  execute format('GRANT CONNECT ON DATABASE %I TO %I',nome_db,nom_usuario);

  --Aqui ele vai receber os dados conforme a role
  case role_usuario when 1 then
         --ADMIN
         execute format('GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA %I TO %I',nome_schema, nom_usuario);
         execute format('GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA %I TO %I',nome_schema, nom_usuario);
         execute format('GRANT ALL PRIVILEGES ON DATABASE %I TO %I',nome_db, nom_usuario);
       
       when 2 then
         --EDITOR
         execute format('GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA %I TO %I',nome_schema,nom_usuario);
         execute format('GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA %I TO %I',nome_schema,nom_usuario);
       
       when 3 then
         --LEITOR
         execute format('GRANT SELECT ON ALL TABLES IN SCHEMA %I TO %I',nome_schema,nom_usuario);
         execute format('GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA %I TO %I',nome_schema,nom_usuario);
       
       else raise exception 'Role de usuário desconhecido: %', role_usuario;
  end case;

end;
$$

LANGUAGE plpgsql;