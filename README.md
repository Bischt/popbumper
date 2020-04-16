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

`pb read machine [all | byid]` - Machine specific operations

`pb [create | update | read | delete] player` - Player specific operations

`pb [create | update | read | delete] location` - Location specific operations

`--no-headers` - Remove headers from output
`--verbose` - Output all info (defaults to simpler display)