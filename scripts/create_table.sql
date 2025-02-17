CREATE SCHEMA stage;

CREATE TABLE stage.brt_gps (
    id                      SERIAL PRIMARY KEY,
    codigo                  VARCHAR(50) NOT NULL,
    placa                   VARCHAR(10),
    linha                   VARCHAR(10),
    latitude                REAL NOT NULL,
    longitude               REAL NOT NULL,
    datahora                TIMESTAMP NOT NULL,
    data                    DATE NOT NULL,
    hora                    TIME NOT NULL,
    velocidade              REAL,
    id_migracao_trajeto     INT,
    sentido                 VARCHAR(25),
    trajeto                 VARCHAR(255),
    hodometro               REAL,
    direcao                 INT,
    ignicao                 REAL
);