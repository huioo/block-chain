import requests

from flask_ver.blocks import block_hash, valid_proof


def valid_chain(chain):
    """
    Determine if a given blockchain is valid

    :return: True if valid, False if not
    """
    previous_block = chain[0]
    current_index = 1
    
    while current_index < len(chain):
        current_block = chain[current_index]
        print(f'{previous_block}')
        print(f'{current_block}')
        print('\n', '-' * 20, '\n')
        
        # Check that the hash of the block is correct
        previous_block_hash = block_hash(previous_block)
        if current_block['previous_hash'] != previous_block_hash:
            return False
        
        # Check that the Proof of Work is correct
        if not valid_proof(previous_block['proof'], current_block['proof'], previous_block_hash):
            return False
        
        previous_block = current_block
        current_index += 1
    
    return True


class BlockChain:
    def __init__(self, block):
        self._blocks = [block]
    

class TransactionBlockChain:
    def __init__(self, block):
        self.chain = [block]
        self.current_transactions = []
    
    @property
    def last_chain(self):
        return self._chain[-1]

    def new_block(self, block):
        self.chain.append(block)
        self.current_transactions = []
        return block

    def add_current_transaction(self, sender, recipient, amount):
        """ 创建新交易记录，添加到下一个将要开采的区块中
        Creates a new transaction to go into the next mined Block

        :param sender: 发送者地址 <str> Address of the Sender
        :param recipient: 接收者地址 <str> Address of the Recipient
        :param amount: 金额 <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_chain['index'] + 1

    def resolve_conflicts(self, neighbours, url_path):
        """
        This is our consensus algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.
        
        :param neighbours: <set> a set of nodes' address
        :param url_path: <str> the url path that is accessible to other node's blockchain
        :return: True if our chain was replaced, False if not
        """
        new_chain = None
        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}{url_path}')
            if response.status_code != 200:
                length = response.json()['length']
                chain = response.json()['chain']
                
                # Check if the length is longer and the chain is valid
                if length > max_length and valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True
        return False


if __name__ == '__main__':
    a = TransactionBlockChain(1)
    print(a.chain)
    a.chain.append(2)
    print(a.chain)

        



