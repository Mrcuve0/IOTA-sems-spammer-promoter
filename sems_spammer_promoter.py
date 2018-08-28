import iota
import sys
import os
from dotenv import load_dotenv, find_dotenv
from iota.crypto.addresses import AddressGenerator


def checkArgs():
    if (len(sys.argv) == 2):
        print('Script in SPAMMER MODE...')
        print('PROMOTER MODE: python3 script.py <http[s]://nodeURL:port> <TH_HASH_to_be_promoted>')
        promoter_mode = False
        tx_hash_to_be_promoted = ""

    elif (len(sys.argv) == 3):
        print('Script in PROMOTER MODE...')
        print('SPAMMER MODE: python3 script.py <http[s]://nodeURL:port>')
        promoter_mode = True
        tx_hash_to_be_promoted = sys.argv[2]

    else:
        print('Error, 2 MODEs allowed:')
        print('     --> PROMOTER MODE: python3 script.py <http[s]://nodeURL:port> <TH_HASH_to_be_promoted>')
        print('     --> SPAMMER MODE: python3 script.py <http[s]://nodeURL:port>')
        sys.exit("Exiting...")
    return (promoter_mode, tx_hash_to_be_promoted)

def printHealth(nodeURL, api):
    print("\n\n### NODE HEALTH ##")
    nodeHealth = api.get_node_info()

    node_appVersion = nodeHealth['appVersion']
    node_latestMilestone = nodeHealth['latestMilestone']
    node_latestMilestoneIndex = nodeHealth['latestMilestoneIndex']
    node_latestSolidSubtangleMilestone = nodeHealth['latestSolidSubtangleMilestone']
    node_latestSolidSubtangleMilestoneIndex = nodeHealth['latestSolidSubtangleMilestoneIndex']
    node_neighbors = nodeHealth['neighbors']
    node_tips = nodeHealth['tips']
    node_transactionsToRequest = nodeHealth['transactionsToRequest']

    print('appVersion: ' + str(node_appVersion))
    print('latestMilestone: ' + str(node_latestMilestone))
    print('latestMilestoneIndex: ' + str(node_latestMilestoneIndex))
    print('latestSolidSubtangleMilestone: ' + str(node_latestSolidSubtangleMilestone))
    print('latestSolidSubtangleMilestoneIndex: ' + str(node_latestSolidSubtangleMilestoneIndex))
    print('neighbors: ' + str(node_neighbors))
    print('tips: ' + str(node_tips))
    print('transactionsToRequest: ' + str(node_transactionsToRequest))

def promoteTX(promoter_mode, rx_address, tx_hash_to_be_promoted, iteration):

    ### TX CREATION ##
    print("\n\n     ### TX CREATION ##")
    if (promoter_mode == True):
        tx_message = "They see me promoting, they hatin!"
        tx_tag = iota.Tag(b'SEMS9PROMOTER9DOT9PY')
    else:
        tx_message = "They see me spamming, they hatin!"
        tx_tag = iota.Tag(b'SEMS9SPAMMER9DOT9PY')
    tx = iota.ProposedTransaction(address = iota.Address(rx_address), 
                                  message = iota.TryteString.from_unicode(tx_message),
                                  tag = tx_tag, 
                                  value = 0)
    print('     Created first transaction: ')
    print("     " + str(vars(tx)))

    ### BUNDLE FINALIZATION ###
    print("\n\n     ### BUNDLE FINALIZATION ###")
    bundle = iota.ProposedBundle(transactions = [tx])
    bundle.finalize()
    print("     Bundle is finalized...")
    print("     Generated bundle hash: %s" % (bundle.hash))
    print("     List of all transaction in the Bundle:\n")
    for txn in bundle:
        print("     " + str(vars(txn)))
    bundle_trytes = bundle.as_tryte_strings() # bundle as trytes

    ### TIP SELECTION ###
    print("\n\n     ### TIP SELECTION ###")
    tips = api.get_transactions_to_approve(depth = 3)
    if (promoter_mode == True):
        tips['branchTransaction'] = tx_hash_to_be_promoted  
    print("     " + str(tips))

    ### POW ###
    print("\n\n     ### POW ###")
    attached_tx = api.attach_to_tangle(trunk_transaction=tips['trunkTransaction'], branch_transaction=tips['branchTransaction'], trytes=bundle_trytes, min_weight_magnitude=14)

    ### BROADCASTING ###
    print("     Broadcasting transaction...")
    res = api.broadcast_and_store(attached_tx['trytes'])
    print("     " + str(res))

    ### TRANSACTION RECAP ###
    print("\n\n     ### TRANSACTION RECAP ###")
    print("     " + str(vars(attached_tx['trytes'][0])))

    sent_tx = iota.Transaction.from_tryte_string(attached_tx['trytes'][0])
    print("     Transaction Hash: " + str(sent_tx.hash))

    if (promoter_mode == True):
        return (sent_tx.hash)
    else:
        return ("")

def destroy(iteration):
    print("     Total iterations: " + iteration)
    print('     Exiting script...')

if __name__ == '__main__':     # Program start from here

        load_dotenv(find_dotenv())

        (promoter_mode, tx_hash_to_be_promoted) = checkArgs()
        if (promoter_mode == True):
            rx_address = os.getenv('RECEIVING_ADDRESS_PROMOTER')
        else:
            rx_address = os.getenv('RECEIVING_ADDRESS_SPAMMER')

        nodeURL = sys.argv[1]
        api = iota.Iota(nodeURL)

        try:
                printHealth(nodeURL, api)    
                iteration = 0
                while True:
                    print("ITERATION #" + str(iteration))
                    tx_hash_to_be_promoted = promoteTX(promoter_mode, rx_address, tx_hash_to_be_promoted, iteration)
                    iteration = iteration + 1
        except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the destroy() will be  executed.
                destroy(iteration)