DROP TABLE IF EXISTS public."Player";

CREATE TABLE public."Player" (
    player_id varchar NOT NULL,
	player_name	varchar Not NULL,
	game_year varchar Not NULL,	
	play_type varchar Not NULL,	
	passing_yards_gained Integer,	
	receiving_yards_gained Integer,
	rushing_yards_gained Integer
	);
