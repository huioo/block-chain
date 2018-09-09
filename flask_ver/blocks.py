"""
区块：block


创建一个新的块，添加到chain中
    Create a new Block in the Blockchain
"""

import time
import json
import hashlib

# from collections import UserDict


class Block:
    """
    
       每一个区块包含它自己本身的一些变量，以及前一个区块的哈希值。这一点非常重要，因为哈希值保证了区块链不可篡改的特性。
    如果一个区块受到攻击哈希值变了，那么后面的所有区块的哈希值都会为之改变。

    """
    
    def __init__(self, index, timestamp, proof, previous_hash, *args, **kwargs):
        # super().__init__(self, *args, **kwargs)
        self.index = index
        self.timestamp = timestamp
        self.proof = proof
        self.previous_hash = previous_hash


class TransactionBlock(Block):
    """
    以下是一个区块的例子：

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
    """
    
    def __init__(self, index, timestamp, transactions, proof, previous_hash):
        """
        Create a new Block in the Blockchain
        
        :param index: <int> 区块的索引
        :param timestamp: <float> 区块的时间戳
        :param transactions: <list> 区块的数据记录，该类区块记录用的的交易记录。每个交易记录的内容有：
            <str> 发送者(sender)
            <str> 接收者(recipient)
            <int> 金额(amount)
        :param proof: <int> POW算法给出的证明
            The proof given by the Proof of Work algorithm
        :param previous_hash: 前一个区块的散列值
            (Optional) <str> Hash of previous Block
        """
        super().__init__(self, index, timestamp, proof, previous_hash)
        self.transactions = transactions if isinstance(transactions, list) else []
    
    def to_dict(self):
        return {
                'index': self.index,
                'timestamp': self.timestamp,
                'transactions': self.transactions,
                'proof': self.proof,
                'previous_hash': self.previous_hash
        }


def block_hash(block):
    """
    Creates a SHA-256 hash of a Block
    :param block: Block
    """
    # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
    block_string = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()


def valid_proof(previous_proof, current_proof, previous_block_hash):
    """
    Validates the Proof
    :param previous_proof: <int> the proof of the Previous Block
    :param current_proof: <int> the proof of the Current Block
    :param previous_block_hash: <str> The hash of the Previous Block
    :return: <bool> True if correct, False if not.
    """
    guess = f'{previous_proof}{current_proof}{previous_block_hash}'
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash.endswith('0000')


def proof_of_work(last_block):
    """
    Simple Proof of Work Algorithm:
     - Find a number p' such that hash(pp') contains leading 4 zeroes
     - Where p is the previous proof, and p' is the new proof

    生成一个区块的后一个区块的proof
    :param last_block: <dict> last Block
    :return: <int>
    """
    last_proof = last_block['proof']
    last_hash = block_hash(last_block)

    proof = 0
    while valid_proof(last_proof, proof, last_hash) is False:
        proof += 1

    return proof
    

def new_block(index, timestamp, transactions, proof, previous_hash):
    return TransactionBlock(
        index, timestamp, transactions, proof, previous_hash
    ).to_json()


def test_new_block():
    transaction = {
        'sender': "8527147fe1f5426f9dd545de4b27ee00",
        'recipient': "a77f5cdfa2934df3954a5c7c7da5df1f",
        'amount': 5,
    }
    return TransactionBlock(
        index=1, timestamp=time.time(), transactions=transaction, proof=324984774000,
        previous_hash='2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824')
    

if __name__ == '__main__':
    TransactionBlock(1,2,3,4,5)
