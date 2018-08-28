# sems-spammer-promoter

## A 2-in-1 script that leverages [Pyota Libraries](https://github.com/iotaledger/iota.lib.py) in order to spam the [IOTA network (Tangle)](http://tangle.glumb.de/) or manually promote a transaction.

### REQUIREMENTS:   
* Pyota libraries
* dotenv

### INSTALLATION:

1. Download code (*Clone or Download* button).
2. Extract zip
3. Open *sems-spammer-promoter-master* folder using ```cd sems-spammer-promoter-master```
4. Install dependencies using ```pip3 install -r requirements.txt```
5. You don't have ```pip3```? You can install by running ```sudo apt install python3-pip``` (Debian-based distros) or ```pacman -S python-pip``` (Manjaro - Arch Linux)
6. Run script (usage below).
7. ???
8. Profit
9. Use ```Ctrl-C``` in order to stop the script.
### USAGE:
* ### Spammer:

    ```python3 sems-spammer-promoter.py <http[s]://nodeURL:port>```

* ### Promoter:
    ```python3 sems-spammer-promoter.py <http[s]://nodeURL:port> <TX_HASH_to_be_approved>```

### HOW DOES IT WORKS?

* ### Spammer:
Using the script in spammer mode allows you to spam meta-transactions (AKA *zero-value transactions*, AKA *messages*) in the IOTA Tangle. 

Sending meta-transactions doesn't need an IOTA Seed, even the receiving Address can be a fake one (check ```.env``` file in the script directory, you can tweak the receiving Addresses as you like, remeber: they must be 81 Chars long)

The script starts by checking the node's health, and will continue even if it's sub-optimal. It's up to you to stop the script and reload it with a different and healthier node. (check https://iotanode.host/ in order to find healthy nodes)
```
- - -
|   |
|   v
|   
|   A meta-transaction is created, then finalized in a bundle. After that 2 random 
|   tips are selected and then used as
|   "branchTransaction" and "trunkTransaction".
|
|   The PoW is performed (some nodes will not let you complete the 
|   "attachToTangle" method, if it's the case, change node and
|   reload the script).
|   
|   The finalized bundle is finally broadcasted to the Tangle.
|
| - - Infinite loop < - -
```

* ### Promoter:
Using the script in promoter mode allows you to manually promote an old transaction


```
- - -
|   |
|   v
|   
|   A meta-transaction is created, then finalized in a bundle. After that 2 random 
|   tips are selected but only one of them will be used as a transaction ("trunkTransaction")
|   the "branchTransaction" will be overwrited with our Transaction Hash of the transaction to be approved.
|
|   The PoW is performed (some nodes will not let you complete the 
|    "attachToTangle" method, if it's the case, change node and
|   reload the script).
|   
|   The finalized bundle is finally broadcasted to the Tangle.
|   The hash of the commited transaction is saved and will be used as the new Transaction Hash of the transaction
|   to be approved. And so on.
| - - Infinite loop < - -
```

Here's a little graph to better understand the procedure:

```                      
                                            . . .    \|                                        |
                                                      \ - - - - -                              |
                                            . . .     |\| trunk |                              |
  \              . . .    \- - - - -                  |/|  TX   |                              |
   \- - - - -              | trunk |                  / | (tip) |                              |
    |       |    . . .     |  TX   |__      . . .    /| - - - - -                              |
    |       |             /| (tip) |  \               |        \- - - - -      branch          |              . . . 
   /|       |            / - - - - -   \              |         | meta  |______________________|
  / - - - - -\   . . .                  \ - - - - -   |         |   -   |        TX            \              . . .
 /            \                         / | meta  |   |        /|  TX   |                      |\ - - - - -
               \                       /  |   -   |  branch   / - - - - -                      | \| meta  |
                - - - - - -           /   |  TX   |_________ /                                 |  |   -   |   . . . 
 \              |    TX   |  branch  /    - - - - -   TX                                       | /|  TX   |
  \             |  to be  |_________/                 |                                        |/ - - - - -
   \- - - - -   |approved.|    TX                     |                \ - - - - -             /
    |       |  /- - - - - -                           |     . . .       \| trunk |            /|
    |       | /                                       |                  |  TX   |___________/ |
   /|       |/                                        |     . . .       /| (tip) |             |
  / - - - - -                                         |                / - - - - -             |
 /                                                    |               /                        |
                                                      |     . . .                              |
                  ---FIRST ITERATION---               |           ---SECOND ITERATION---       | ---THIRD 
                                                                                                    ITERATION---