-- Criação da sequência para id_residencia
CREATE SEQUENCE residencia_seq
START WITH 1
INCREMENT BY 1
NOCACHE
NOCYCLE;

-- Criação da sequência para id_historico
CREATE SEQUENCE historico_seq
START WITH 1
INCREMENT BY 1
NOCACHE
NOCYCLE;

-- Criação da tabela residencias
CREATE TABLE residencias (
    id_residencia       NUMBER PRIMARY KEY,
    nome_responsavel    VARCHAR2(100) NOT NULL,
    endereco            VARCHAR2(200) NOT NULL,
    capacidade_geracao  NUMBER(10, 2),  -- Capacidade de geração em kWh
    tipo_fonte          VARCHAR2(50),   -- Ex: 'Solar', 'Eólica', etc.
    limite_consumo      NUMBER(10, 2),  -- Limite de consumo em kWh
    data_cadastro       DATE DEFAULT SYSDATE
);

-- Criação da tabela historico_energia
CREATE TABLE historico_energia (
    id_historico        NUMBER PRIMARY KEY,
    id_residencia       NUMBER REFERENCES residencias(id_residencia),
    data_registro       DATE NOT NULL,
    producao            NUMBER(10, 2) NOT NULL,  -- Produção de energia em kWh
    consumo             NUMBER(10, 2) NOT NULL,  -- Consumo de energia em kWh
    saldo_energetico    NUMBER(10, 2)           -- Produção - Consumo
);
