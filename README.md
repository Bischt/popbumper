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

`pb create` - Create operations

`pb read` - Read operations

`pb update` - Update operations

`pb delete` - Delete operations

`pb read machine [all | by_id | by_name | by_abbr | by_manufacturer] [<value>]` - Machine read operations

`pb read player [all | by_id | by_name] [<value>]` - Player read operations

`pb read location [all | by_id | by_name] [<value>]` - Location read operations

`--no-headers` - Remove headers from output
`--verbose` - Output all info (defaults to simpler display)