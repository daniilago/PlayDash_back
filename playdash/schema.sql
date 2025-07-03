CREATE TABLE user (
    name character varying(30) NOT NULL,
    email text NOT NULL,
    password character varying(50) NOT NULL,
    user_type character(1) NOT NULL DEFAULT 'U',

    CONSTRAINT user_pkey PRIMARY KEY (email)
);

CREATE TABLE team (
    name character varying(100) NOT NULL,
    emblem text NOT NULL,
    match_total integer NOT NULL DEFAULT 0,
    points_total integer NOT NULL DEFAULT 0,
    fouls integer NOT NULL DEFAULT 0,
    yellow_cards integer NOT NULL DEFAULT 0,
    red_cards integer NOT NULL DEFAULT 0,
    wins integer NOT NULL DEFAULT 0,
    draws integer NOT NULL DEFAULT 0,
    losses integer NOT NULL DEFAULT 0,
    own_goals integer NOT NULL DEFAULT 0,
    against_goals integer NOT NULL DEFAULT 0,

    CONSTRAINT team_pkey PRIMARY KEY (name)
);

CREATE TABLE player (
    name character varying(100) NOT NULL,
    date_of_birth date NOT NULL,
    nationality character varying(20) NOT NULL,
    photo text NOT NULL,
    goals integer NOT NULL DEFAULT 0,
    position character varying(30) NOT NULL,
    shirt_number integer NOT NULL,
    fouls integer NOT NULL DEFAULT 0,
    yellow_cards integer NOT NULL DEFAULT 0,
    red_cards integer NOT NULL DEFAULT 0,
    team_name character varying(100) NOT NULL,

    CONSTRAINT player_pkey PRIMARY KEY (shirt_number, team_name),
    CONSTRAINT player_team_name_fkey FOREIGN KEY (team_name) 
        REFERENCES team(name) 
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE coach (
    name character varying(100) NOT NULL,
    date_of_birth date NOT NULL,
    nationality character varying(20) NOT NULL,
    photo text NOT NULL,
    team_name character varying(100) NOT NULL,

    CONSTRAINT coach_pkey PRIMARY KEY (name),
    CONSTRAINT coach_team_name_fkey FOREIGN KEY (team_name) 
        REFERENCES team(name) 
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE match (
    id integer NOT NULL,
    date_hour timestamp NOT NULL,
    location character varying(100) NOT NULL,
    home_team character varying(100) NOT NULL,
    visitor_team character varying(100) NOT NULL,
    home_goals integer NOT NULL DEFAULT 0,
    visitor_goals integer NOT NULL DEFAULT 0,

    CONSTRAINT match_pkey PRIMARY KEY (id),
    CONSTRAINT match_home_team_name_fkey FOREIGN KEY (home_team) 
        REFERENCES team(name)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT match_visitor_team_name_fkey FOREIGN KEY (visitor_team) 
        REFERENCES team(name)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE event (
    id integer NOT NULL,
    match_id integer NOT NULL,
    date_hour timestamp NOT NULL,
    player_number integer NOT NULL,
    player_team character varying(100) NOT NULL,
    event_type character varying(20) NOT NULL,

    CONSTRAINT event_pkey PRIMARY KEY (id, match_id),
    CONSTRAINT event_match_id_fkey FOREIGN KEY (match_id) 
        REFERENCES match(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT event_player_number_player_team_fkey FOREIGN KEY (player_number, player_team)
        REFERENCES player(shirt_number, team_name)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TRIGGER update_player_stats_after_event
AFTER INSERT ON event
BEGIN
    UPDATE player
    SET goals = goals + 1
    WHERE shirt_number = NEW.player_number
      AND team_name = NEW.player_team
      AND NEW.event_type = 'gol';

    UPDATE player
    SET yellow_cards = yellow_cards + 1
    WHERE shirt_number = NEW.player_number
      AND team_name = NEW.player_team
      AND NEW.event_type = 'cartao_amarelo';

    UPDATE player
    SET red_cards = red_cards + 1
    WHERE shirt_number = NEW.player_number
      AND team_name = NEW.player_team
      AND NEW.event_type = 'cartao_vermelho';

    UPDATE player
    SET fouls = fouls + 1
    WHERE shirt_number = NEW.player_number
      AND team_name = NEW.player_team
      AND NEW.event_type = 'falta';
END;

CREATE TRIGGER update_team_stats_after_event
AFTER INSERT ON event
BEGIN
    UPDATE team
    SET own_goals = own_goals + 1
    WHERE name = NEW.player_team AND NEW.event_type = 'gol';

    UPDATE team
    SET fouls = fouls + 1
    WHERE name = NEW.player_team AND NEW.event_type = 'falta';

    UPDATE team
    SET yellow_cards = yellow_cards + 1
    WHERE name = NEW.player_team AND NEW.event_type = 'cartao_amarelo';

    UPDATE team
    SET red_cards = red_cards + 1
    WHERE name = NEW.player_team AND NEW.event_type = 'cartao_vermelho';
END;

CREATE TRIGGER update_team_against_goals_after_event
AFTER INSERT ON event
BEGIN
    UPDATE team
    SET against_goals = against_goals + 1
    WHERE name IN (
        SELECT CASE
            WHEN m.home_team = NEW.player_team THEN m.visitor_team
            WHEN m.visitor_team = NEW.player_team THEN m.home_team
        END
        FROM match m
        WHERE m.id = NEW.match_id
    )
    AND NEW.event_type = 'gol';
END;

CREATE TRIGGER update_match_goals_after_event
AFTER INSERT ON event
BEGIN
    -- Gols do time da casa
    UPDATE match
    SET home_goals = home_goals + 1
    WHERE id = NEW.match_id
      AND home_team = NEW.player_team
      AND NEW.event_type = 'gol';

    -- Gols do time visitante
    UPDATE match
    SET visitor_goals = visitor_goals + 1
    WHERE id = NEW.match_id
      AND visitor_team = NEW.player_team
      AND NEW.event_type = 'gol';
END;

CREATE TRIGGER update_team_stats_after_match
AFTER INSERT ON match
BEGIN
    -- Total de partidas
    UPDATE team
    SET match_total = match_total + 1
    WHERE name = NEW.home_team OR name = NEW.visitor_team;

    -- Vitórias, empates, derrotas e pontos para o time da casa
    UPDATE team
    SET wins = wins + CASE WHEN NEW.home_goals > NEW.visitor_goals THEN 1 ELSE 0 END,
        draws = draws + CASE WHEN NEW.home_goals = NEW.visitor_goals THEN 1 ELSE 0 END,
        losses = losses + CASE WHEN NEW.home_goals < NEW.visitor_goals THEN 1 ELSE 0 END,
        points_total = points_total + CASE
            WHEN NEW.home_goals > NEW.visitor_goals THEN 3
            WHEN NEW.home_goals = NEW.visitor_goals THEN 1
            ELSE 0 END
    WHERE name = NEW.home_team;

    -- Vitórias, empates, derrotas e pontos para o time visitante
    UPDATE team
    SET wins = wins + CASE WHEN NEW.visitor_goals > NEW.home_goals THEN 1 ELSE 0 END,
        draws = draws + CASE WHEN NEW.home_goals = NEW.visitor_goals THEN 1 ELSE 0 END,
        losses = losses + CASE WHEN NEW.visitor_goals < NEW.home_goals THEN 1 ELSE 0 END,
        points_total = points_total + CASE
            WHEN NEW.visitor_goals > NEW.home_goals THEN 3
            WHEN NEW.home_goals = NEW.visitor_goals THEN 1
            ELSE 0 END
    WHERE name = NEW.visitor_team;
END;