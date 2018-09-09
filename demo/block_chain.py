import json
import time
import hashlib
import requests

from urllib import parse


class BlockChain:
    """
    Blockchain 参数的作用是`管理区块链`，也用于`存储交易信息`和`添加区块的方式`。

    什么是区块链？
        区块链是由不可变的、有顺序记录的区块组成。他们可以包含交易数据、文件数据或者其他你想要记录的数据。
        不过最重要的是这些区块通过哈希表链接在一起。
    """

    def __init__(self):
        self.chain = []    # 存储区块链
        self.current_transactions = []    # 存储交易
        # 创建创世区块
        self.new_block(previous_hash=1, proof=100)
        # 节点
        self.nodes = set()

    @property
    def last_block(self):
        """ 返回chain中最后的块 """
        return self.chain[-1]

    def new_block(self, proof, previous_hash=None):
        """  Create a new Block in the Blockchain
        创建一个新的块，添加到chain中

        每一个区块包含一个索引、一个时间戳、一个交易列表、一个证明（之后更多）和前一个区块的哈希值。  
        以下是一个区块的例子：
        ```
        block = {
            'index': 1,
            'timestamp': 1506057125.900785,
            'transactions': [
                {
                    'sender': "8527147fe1f5426f9dd545de4b27ee00",
                    'recipient': "a77f5cdfa2934df3954a5c7c7da5df1f",
                    'amount': 5,
                }
            ],
            'proof': 324984774000,
            'previous_hash': "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
        }
        ```
        每一个区块包含它自己本身的一些变量，以及前一个区块的哈希值。这一点非常重要，因为哈希值保证了区块链不可篡改的特性。如果一个区块受到攻击哈希值变了，那么后面的所有区块的哈希值都会为之改变。

        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }
        # Reset the current list of transactions
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined Block
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        """
        self.current_transactions.append(
            {
                'sender': sender,
                'recipient': recipient,
                'amount': amount
            }
        )
        return self.last_block['index'] + 1

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == '0000'

    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work Algorithm:
        - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
        - p is the previous proof, and p' is the new proof
        
        :param last_proof: <int>
        :return: <int>
        """
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1
        return proof

    def register_node(self, address):
        """
        Add a new node to the list of nodes
        :param address: <str> Address of node. Eg. 'http://192.168.0.5:5000'
        :return: None
        """
        parsed_url = parse.urlparse(address)
        self.nodes.add(parsed_url.netloc)
        
    @staticmethod
    def hash(block):
        """  什么是散列？
        散列函数是一个输入值函数，从该输入创建一个确定输入值的输出值。
    
        更多解释可以点击下边这个链接：
        https://learncryptography.com/hash-functions/what-are-hash-functions
    
        Creates a SHA-256 hash of a Block
        :param block: <dict> Block
        :return: <str>
        """
        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid
        :param chain: <list> A blockchain
        :return: <bool> True if valid, False if not
        """
        last_block = chain[0]
        current_index = 1
        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}', f'{block}', '-'*20, sep='\n')
    
            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False
            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False
            
            last_block = block
            current_index += 1
        return True
    
    def resolve_conflicts(self):
        """
        This is our Consensus Algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.
        :return: <bool> True if our chain was replaced, False if not
        """
        neighbours = self.nodes
        new_chain = None
        # We're only looking for chains longer than ours
        max_length = len(self.chain)
        
        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                
                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain
        
        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True
        else:
            return False
