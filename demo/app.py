import uuid

from flask import Flask, jsonify, request

from demo.block_chain import BlockChain

# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid.uuid4().hex)

# Instantiate the Blockchain
MY_BLOCK_CHAIN = BlockChain()


@app.route('/mine', methods=['GET'])
def mine():
    """ 告诉我们的服务器开采一个新的区块
    
    创建 /mine 端点，这是一个GET请求 """
    # We run the proof of work algorithm to get the next proof...
    last_block = MY_BLOCK_CHAIN.last_block
    last_proof = last_block['proof']
    proof = MY_BLOCK_CHAIN.proof_of_work(last_proof)
    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    MY_BLOCK_CHAIN.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )
    # Forge the new Block by adding it to the chain
    previous_hash = MY_BLOCK_CHAIN.hash(last_block)
    block = MY_BLOCK_CHAIN.new_block(proof, previous_hash)
    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    """ 为一个区块创建一个新的交易
    
    创建 /transactions/new 端点，这是一个 POST 请求，我们将用它来发送数据 """
    values = request.get_json()
    # Check that the required fields are in the POST'ed data
    print(values)
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
    
    # Create a new Transaction
    index = MY_BLOCK_CHAIN.new_transaction(**values)
    response = {
        'message': f'Transaction will be added to Block {index}'
    }
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    """ 返回完整的 Blockchain 类
    
    创建 /chain 端点，它是用来返回整个 Blockchain 类 """
    response = {
        'chain': MY_BLOCK_CHAIN.chain,
        'length': len(MY_BLOCK_CHAIN.chain)
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        MY_BLOCK_CHAIN.register_node(node)
    response = {
        'message': 'New nodes have been added.',
        'total_nodes': list(MY_BLOCK_CHAIN.nodes)
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = MY_BLOCK_CHAIN.resolve_conflicts()
    response = {
        'new_chain': MY_BLOCK_CHAIN.chain
    }
    
    if replaced:
        response['message'] = 'Our chain was replaced'
    else:
        response['message'] = 'Our chain is authoritative'
    return jsonify(response), 200
    
    
@app.route('/')
def helloworld():
    return 'hello, world!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

"""
交易的请求是什么形式呢？下面我们看看用户发送到服务器的一段请求代码：
{
    "sender": "my address",
    "recipient": "someone else's address",
    "amount": 5
}
"""
