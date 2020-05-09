pop bumper
==========
A command line client

Description:
------------
Command line client for the playfield API.  Used primarily to develop and test the API but could also be used as a 
simple command line client.

Usage:
------
`pb help` - Display help

`pb health` - Health check back end system

Commands will begin with `pb` and have the values shown in the tables below:

#### Machines

| Action   | Subject   | Operation         | Parameters   | Description                                      |
| :------- |:--------- | :---------------- | :----------- | :----------------------------------------------: |
| `read`   | `machine` | `all`             |              | List all machines                                |
| `read`   | `machine` | `by_id`           | machine_id   | List machines with provided ID                   |
| `read`   | `machine` | `by_name`         | name         | List machines with provided name                 |
| `read`   | `machine` | `by_abbr`         | abbr         | List machines with provided abbr                 |
| `read`   | `machine` | `by_manufacturer` | manufacturer | List machines with provided manufacturer         |
| `create` | `machine` |                   |              | Create new machine                               |
| `update` | `machine` |                   | machine_id   | Update machine with provided ID                  |
| `delete` | `machine` |                   | machine_id   | Remove machine with provided ID                  |

#### Players

| Action   | Subject   | Operation         | Parameters   | Description                                      |
| :------- |:--------- | :---------------- | :----------- | :----------------------------------------------: |
| `read`   | `player`  | `all`             |              | List all players                                 |
| `read`   | `player`  | `active`          |              | List all active players                          |
| `read`   | `player`  | `by_id`           | player_id    | List players with provided ID                    |
| `read`   | `player`  | `name`            | name         | List players with provided name                  |
| `create` | `player`  |                   |              | Create new player                                |
| `update` | `player`  |                   | player_id    | Update player with provided ID                   |
| `update` | `player`  | `set_status`      | player_id, integer      | Update player status with provided ID to integer |
| `update` | `player`  | `set_active`      | player_id, boolean      | Update player active with provided ID to boolean |
| `delete` | `player`  |                   | player_id    | Remove player with provided ID                   |

#### Locations

| Action   | Subject    | Operation         | Parameters   | Description                                      |
| :------- |:---------- | :---------------- | :----------- | :----------------------------------------------: |
| `read`   | `location` | `all`             |              | List all locations                               |
| `read`   | `location` | `playable`        |              | List active locations with actie gamecount       |
| `read`   | `location` | `by_id`           | location_id  | List locations with provided ID                  |
| `read`   | `location` | `name`            | name         | List locations with provided name                |
| `read`   | `location` | `all_machines`    | location_id  | List all machines at location                    |
| `read`   | `location` | `active_machines` | location_id  | List all ACTIVE machine at location              |
| `create` | `location` |                   |              | Create a new location                            |
| `create` | `location` | `add_game`        | location_id, game_id  | Add machine to location                          |
| `update` | `location` |                   | location_id  | Update location with provided ID                 |
| `update` | `location` | `game`            | game_id      | Update machine on location                       |
| `update` | `location` | `game_active`     | game_id      | Set active on location game                      |
| `update` | `location` | `set_active`      | location_id, boolean      | Update location active with provided ID to boolean |
| `delete` | `location` |                   | location_id  | Remove location with provided ID                 |
| `delete` | `location` | `game_from`       | game_id, location_id      | Remove game from location                        |


#### Tournaments

| Action   | Subject      | Operation         | Parameters    | Description                                      |
| :------- |:------------ | :---------------- | :------------ | :----------------------------------------------: |
| `read`   | `tournament` | `all`             |               | List all tournaments                             |
| `read`   | `tournament` | `active`          |               | List all active tournaments                      |
| `read`   | `tournament` | `by_id`           | tournament_id | List tournament by ID                            |
| `read`   | `tournament` | `by_name`         | name          | List tournament by name                          |
| `read`   | `tournament` | `by_location`     | location_id   | List all tournaments at provided location        |
| `read`   | `tournament` | `get_players`     | tournament_id | List all players added to tournament ID          |
| `create` | `tournament` |                   |               | Create a new tournament                          |
| `create` | `tournament` | `add_player`      | tournament_id, player_id | Add a player to the tournament        |
| `update` | `tournament` |                   | tournament_id | Update a tournament                              |
| `update` | `tournament` | `set_active`      | tournament_id, boolean | Update tournament active with provided ID to boolean |
| `delete` | `tournament` |                   | tournament_id | Remove tournament with provided ID               |
| `delete` | `tournament` | `remove_player`   | tournament_id, player_id | Remove player by ID from tournament by ID |

#### Tournament Series

`--no-headers` - Remove headers from output
`--verbose` - Output all info (defaults to simpler display)