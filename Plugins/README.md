# Exploit disclosure

## Godmode: forced time desync-resync

Darza's Dominion has a server-sided bullet simulation. This means if you get hit by a bullet but prevent the client from telling the server, the simulation will still predict you to be at the location of the bullet and apply the damage anyways. As a result, any vulnerabilities would need to attack where the server actually thinks you are.

- Exploit: If you add a fixed amount of time (around two to five seconds) to the Move packet, the server will simulate the bullet incorrectly. You will disconnect after a while; you seem to not disconnect at all when there are a lot of players. See [Godmode.py](https://github.com/swrlly/Midnight/blob/main/Plugins/Gdomode.py) for this exploit.
