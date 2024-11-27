-- Apaga o banco de dados.
-- PERIGO! Só use isso em modo de desenvolvimento.
DROP DATABASE IF EXISTS blocodenotas;

-- Cria o banco de dados "novamente".
-- PERIGO! Só use isso em modo de desenvolvimento.
CREATE DATABASE blocodenotas
    -- Seleciona a tabela de caracteres UTF-8 (acentuação).
    CHARACTER SET utf8mb4
    -- Permite buscas case-insensitive (A=a, ç=c, ã=a).
    COLLATE utf8mb4_unicode_ci;

-- Seleciona o banco de dados
-- Todos comandos seguintes sejam para este banco de dados
USE blocodenotas;

-- Cria a tabela da entidade "usuario"
-- Prefixo dos atributos → u_
CREATE TABLE usuario (
    u_id INT PRIMARY KEY AUTO_INCREMENT,
    u_data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    u_nome VARCHAR(127) NOT NULL,
    u_nascimento DATE NOT NULL,
    u_email VARCHAR(255) NOT NULL,
    u_senha VARCHAR(63) NOT NULL,
    u_status ENUM ('on', 'off', 'del') DEFAULT 'on'
);

-- Cria a tabela da entidade "treco"
-- Prefixo dos atributos → t_
CREATE TABLE notas (
    t_id INT PRIMARY KEY AUTO_INCREMENT,
    t_data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    t_usuario INT NOT NULL,
    t_nome VARCHAR(127) NOT NULL,
    t_anotacao TEXT,
    t_status ENUM ('on', 'off', 'del') DEFAULT 'on',
    FOREIGN KEY (t_usuario) REFERENCES usuario(u_id)
);

-- -------------------------------------- --
-- Insere alguns dados "fake" nas tabelas --
-- -------------------------------------- --

-- Tabela 'usuario'
INSERT INTO usuario (
    u_nome,
    u_nascimento,
    u_email,
    u_senha
) VALUES (
    'Joca da Silva',
    '2000-04-25',
    'jocasilva@email.com',
    SHA1('Senha123') -- Criptografa a senha do usuário
), (
    'Marineuza Siriliano',
    '2003-03-12',
    'marineuza@email.com',
    SHA1('Senha123')
), (
    'Setembrino Trocatapas',
    '1998-12-14',
    'setbrino@email.com',
    SHA1('Senha123')
);


INSERT INTO notas (
    t_usuario,
    t_nome,
    t_anotacao
) VALUES ( 
    '1',
    'Não esquecer de jogar o lixo pra fora', 
    'Na estante da sala, prateleira de baixo tem uma lata de leite em pó.'
), (
    '2',
    'Não esquecer de estudar matemática as 16 horas.',
    'sair hoje ás 15 horas da tarde.'
);

