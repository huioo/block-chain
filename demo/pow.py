"""
the Proof of Work algorithm

关于工作量证明(PoW）

工作证明算法（PoW）的作用，是对区块链上创建或开发新的区块的证明。
其背后的核心是：找到一串解决某个数学问题的数字，这个数字必须符合两个条件：第一，难找；第二，很容易被验证（而且是很容易被任何人验证）。


"""

from hashlib import sha256


def demo1(x=5, y=0):
    """
    我们来看一下这个例子，某个整数 x 乘以另外一个数 y ，得到的结果的哈希值必须是以 0 结尾。可以简单表示为：hash(x * y) = ac23dc...0。
    所以，我们的目标是找到满足这个条件的一个 y 值。
    为了方便理解，我们暂定x=5。

    最终，计算结果是 y=21。因此，生成的以 0 结尾的哈希值是：1253e9373e781b7500266caa55150e08e210bc8cd8cc70d89985e3600155e860

    在比特币中，PoW算法被称为Hashcash，原理跟上面例子差不多。
    矿工们为了能创建一个新区块，铆足劲儿做着上面的数学题（只有胜出者才能添加区块）。
    一般而言，证明的难度取决于字符串中搜索的字符数量，先找到正确数字的旷工就能够在每笔交易中获得比特币作为奖励。

    系统能够很容易验证他们的解决方案。
    """
    while sha256(f'{x*y}'.encode()).hexdigest()[-1] != '0':
        y += 1
    
    print(f'The solution is y = {y}')
    print(sha256(f'{x*y}'.encode()).hexdigest())


def demo2(last_proof, proof):
    """
    我们可以通过修改哈希值前 0 的数量，来调整算法的难度，一般来说，4位已经是足够了。
    每在哈希值前多加一个0，计算所花费的时间将呈指数倍增加。
    
    :param last_proof: <int> Previous Proof
    :param proof: <int> Current Proof
    :return:
    """
    valid_proof = False
    while not valid_proof:
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = sha256(guess).hexdigest()
        if guess_hash[:4] == '0000':
            valid_proof = True
        proof += 1
    return proof
    

