# EVO-Summer-Python-Lab-18
EVO Summer Python Lab'18
Simulation has 3 custom modes:
  - my_gossip
  - my_gossip_split (best)
  - my_gossip100
Standart:
  - gossip
To use some of it, just write arguments after filepath.
Example:
python Simulate.py -n 20 -i 1000 --my-gossip --my-gossip-split

Description:
  -my_gossip - added randomising without self-choosing
  -my_gossip_split - in addition to my_gossip has list splitting, it splits list on 2 parts and determines new randomise scope.
  -my_gossip100 - it creates new list for visited nodes and ignore them for future package sending.
