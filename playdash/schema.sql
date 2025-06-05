CREATE TABLE usuario (
    nome_usuario character varying(30) NOT NULL,
    email text NOT NULL,
    senha character varying(50) NOT NULL,
    tipo_do_usuario character(1) NOT NULL DEFAULT 'U',

    CONSTRAINT usuario_pkey PRIMARY KEY (email)
);

CREATE TABLE "time" (
    nome_time character varying(100) NOT NULL,
    brasao text NOT NULL,
    total_partidas integer NOT NULL DEFAULT 0,
    total_pontos integer NOT NULL DEFAULT 0,
    faltas integer NOT NULL DEFAULT 0,
    cartoes_amarelos_time integer NOT NULL DEFAULT 0,
    cartoes_vermelhos_time integer NOT NULL DEFAULT 0,
    vitorias integer NOT NULL DEFAULT 0,
    empates integer NOT NULL DEFAULT 0,
    derrotas integer NOT NULL DEFAULT 0,
    gols_pro integer NOT NULL DEFAULT 0,
    gols_contra integer NOT NULL DEFAULT 0,

    CONSTRAINT time_pkey PRIMARY KEY (nome_time)
);

CREATE TABLE jogador (
    nome_jogador character varying(100) NOT NULL,
    data_nascimento timestamp NOT NULL,
    nacionalidade character varying(20) NOT NULL,
    foto text NOT NULL,
    gols integer NOT NULL DEFAULT 0,
    posicao character varying(30) NOT NULL,
    numero integer NOT NULL,
    faltas integer NOT NULL DEFAULT 0,
    cartoes_amarelos integer NOT NULL DEFAULT 0,
    cartoes_vermelhos integer NOT NULL DEFAULT 0,
    nome_time character varying(100) NOT NULL,

    CONSTRAINT jogador_pkey PRIMARY KEY (numero, nome_time),
    CONSTRAINT jogador_nome_time_fkey FOREIGN KEY (nome_time) 
        REFERENCES "time"(nome_time)
);

CREATE TABLE tecnico (
    nome_tecnico character varying(100) NOT NULL,
    data_nascimento timestamp without time zone NOT NULL,
    nacionalidade character varying(20) NOT NULL,
    foto text NOT NULL,
    nome_time character varying(100) NOT NULL,

    CONSTRAINT tecnico_pkey PRIMARY KEY (nome_time),
    CONSTRAINT tecnico_nome_time_fkey FOREIGN KEY (nome_time) 
        REFERENCES "time"(nome_time)
);

CREATE TABLE partida (
    id_partida integer NOT NULL,
    data_horario timestamp without time zone NOT NULL,
    local_partida character varying(100) NOT NULL,
    time_casa_nome character varying(100) NOT NULL,
    time_visitante_nome character varying(100) NOT NULL,
    gols_casa integer NOT NULL DEFAULT 0,
    gols_visitante integer NOT NULL DEFAULT 0,

    CONSTRAINT partida_pkey PRIMARY KEY (id_partida),
    CONSTRAINT partida_time_casa_nome_fkey FOREIGN KEY (time_casa_nome) 
        REFERENCES "time"(nome_time),
    CONSTRAINT partida_time_visitante_nome_fkey FOREIGN KEY (time_visitante_nome) 
        REFERENCES "time"(nome_time)
);

CREATE TABLE evento (
    id_evento integer NOT NULL,
    id_partida integer NOT NULL,
    data_horario timestamp without time zone NOT NULL,
    jogador_numero integer NOT NULL,
    jogador_time character varying(100) NOT NULL,
    tipo_do_evento character varying(20) NOT NULL,

    CONSTRAINT evento_pkey PRIMARY KEY (id_evento, id_partida),
    CONSTRAINT evento_id_partida_fkey FOREIGN KEY (id_partida) 
        REFERENCES partida(id_partida),
    CONSTRAINT evento_jogador_numero_jogador_time_fkey FOREIGN KEY (jogador_numero, jogador_time)
        REFERENCES jogador(numero, nome_time)
);