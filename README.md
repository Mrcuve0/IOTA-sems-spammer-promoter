# sems-spammer-promoter

## A 2-in-1 script that leverages [Pyota Libraries](https://github.com/iotaledger/iota.lib.py) in order to spam the [IOTA network (Tangle)](http://tangle.glumb.de/) or manually promote a transaction.

[![DevelopmentStatus](https://img.shields.io/badge/Development-Paused-yellow.svg)](https://img.shields.io/badge/Development-Paused-yellow.svg)
[![HitCount](http://hits.dwyl.io/Mrcuve0/IOTA-sems-spammer-promoter.svg)](http://hits.dwyl.io/Mrcuve0/IOTA-sems-spammer-promoter)

![Twitter Follow](https://img.shields.io/twitter/follow/Mrcuve0?label=Follow%20Me%21%20%40Mrcuve0&style=social)

### DISCLAIMER:
This project is for experimental purposes only, bugs may be present, and many python rules may not be followed. I'm still learning about IOTA and Python so don't expect too much.
I do not take responsibility for any damages caused or funds lost (should not be the case, since sending meta-transactions does not require seed)

Having said that, feel free to make changes to the code or suggest improvements to the script, I would like to learn as much as possible and in the best possible way.

Remember that spamming when not explicitly required by the IOTA Foundation is only counterproductive as it significantly increases the storage space occupied by the Tangle, making snapshots more frequent and slowing down the rest of the development.

The idea of the promoter was born after the various bugs related to "inconsistent subtangle", present in IRI 1.5.3.

If you've learned something from this project or if I've been nice, you might consider a donation at ```OSYUR9NE9SV9LYGFWOAWAPXSQCXEITZXRKHSVSXIKYXUUSGIMIJZMSKCXZBVZRYUVMVS9KYNENVZVVULADJWOUUYBX```.

![Address QRCODE.png](https://github.com/Mrcuve0/sems-spammer-promoter/blob/master/Address%20QRCODE.png)

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
|   The PoW is performed (some nodes will not let you complete the "attachToTangle" method, 
|   if it's the case, change node and reload the script).
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
|   tips are selected but only one of them will be used as a transaction ("trunkTransaction").
|   The "branchTransaction" will be overwrited with our Transaction Hash of the transaction to be approved.
|
|   The PoW is performed (some nodes will not let you complete the 
|    "attachToTangle" method, if it's the case, change node and
|   reload the script).
|   
|   The finalized bundle is finally broadcasted to the Tangle.
|   The hash of the commited transaction is saved and will be used as the new Transaction Hash of the 
|   transaction to be approved. And so on.
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
```                                                                                        

### SOME COMMENTS:

* ### Spammer:
    Probably needs code refinement, but the algorithm is pretty straight-forward.
    Can be improved by adding a PoW as-a-service implementation, in order to enhance the throughput (TPS aka *Transaction Per Second*).

* ### Promoter:
    Needs code refinement, the algorithm is working but there's probably a better implementation that guarantees better timings. Should be noted that this implementation avoids blowballs on milestones, but creates a chain of *meta-transactions*.
    Sometimes, better timings are achieved by launching the script in 2 or more parallel sessions (also with different nodes). This could be better implemented by launching the infinite loop in multiple threads, probably new versions of the script will explore this solution.

    And now, some examples of correctly promoted transactions:

    https://thetangle.org/transaction/OHATVIEHDOIQGBLNUSYAXZZDGT9RTJSPOLOQDZSHVGSVBXLFFTZROBWHGSRUMBEXTZOSGKWGGHOCA9999
    
    ```promoted by... ```
    
    https://thetangle.org/transaction/QNZJPBALYGTBZRMKYLMQLVGMXRYCOSFCIXHTDVBULYDNHBX9MPVNEMKYICVNBLACTDOEFDRTDOSEA9999

    ```or...```

    https://thetangle.org/transaction/YJZANSPQCA9XIJUAWJSZUXBJBXVJEUDPWNLGH9SXIAJGAXLOQCJPFTBCWTHPHJCEFJFLUBBVOAVLZ9999

    ```promoted by... ```

    https://thetangle.org/transaction/LAVSJGOSOMUOFEWKD9DHQNLBPOJOF9EFMFRBW9BNGJVAKWKGBJQSD9WCNVJLEMKWEJBHCWUPELKBA9999

    and many, many others. 
    
    In just 2 hours I confirmed transactions for about 4Gi, randomly picked between pending transactions found on https://tanglemonitor.com/.