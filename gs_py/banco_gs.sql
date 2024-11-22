-- Cria��o da sequ�ncia para id_residencia
CREATE SEQUENCE residencia_seq
START WITH 1
INCREMENT BY 1
NOCACHE
NOCYCLE;

-- Cria��o da sequ�ncia para id_historico
CREATE SEQUENCE historico_seq
START WITH 1
INCREMENT BY 1
NOCACHE
NOCYCLE;

-- Cria��o da tabela residencias
CREATE TABLE residencias (
    id_residencia       NUMBER PRIMARY KEY,
    nome_responsavel    VARCHAR2(100) NOT NULL,
    endereco            VARCHAR2(200) NOT NULL,
    capacidade_geracao  NUMBER(10, 2),  -- Capacidade de gera��o em kWh
    tipo_fonte          VARCHAR2(50),   -- Ex: 'Solar', 'E�lica', etc.
    limite_consumo      NUMBER(10, 2),  -- Limite de consumo em kWh
    data_cadastro       DATE DEFAULT SYSDATE
);

-- Cria��o da tabela historico_energia
CREATE TABLE historico_energia (
    id_historico        NUMBER PRIMARY KEY,
    id_residencia       NUMBER REFERENCES residencias(id_residencia),
    data_registro       DATE NOT NULL,
    producao            NUMBER(10, 2) NOT NULL,  -- Produ��o de energia em kWh
    consumo             NUMBER(10, 2) NOT NULL,  -- Consumo de energia em kWh
    saldo_energetico    NUMBER(10, 2)           -- Produ��o - Consumo
);
