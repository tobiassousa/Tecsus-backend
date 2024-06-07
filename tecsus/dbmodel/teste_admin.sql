--Conectar ao banco de dados
\c postgres

CREATE TABLE IF NOT EXISTS teste_operacoes (
    id SERIAL PRIMARY KEY,
    descricao VARCHAR(100)
);

declare
  
  v_user := 'nome_usuario';


-- Conectar como usuario
\c postgres v_user

-- Testar SELECT
SELECT * FROM teste_operacoes;

-- Testar INSERT (Caso não seja admin ou editor, é esperado erro)
INSERT INTO teste_operacoes (descricao) VALUES ('insert test');

-- Testar UPDATE (Caso não seja admin ou editor, é esperado erro)
UPDATE teste_operacoes SET descricao = 'update test' WHERE id = 1;

-- Testar DELETE (Caso não seja admin, é esperado erro)
DELETE FROM teste_operacoes WHERE id = 1;
