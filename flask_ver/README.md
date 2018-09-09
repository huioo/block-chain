
nodes -> 某个node  
> node -> 存在一个blockchain  
>> blockchain -> 存在有顺序的block  
>>> block -> 包含区块的信息，数据信息等  

```python
node = {
    'nodes': {
        'address1', 'address2', ...
    }
}

blockchain = [
    {
        'index': <int>,
        'timestamp': <float>,
        'transactions': [
            {
                'sender': 'address of sender',
                'recipient': 'address of recipient',
                'amount': <int>
            },
            ...
        ]
        'proof': <int>,
        'previous_hash': <base-16 str>
    },
    ...
]

# 用于生成下一个block时，作为transactions的值
blockchain.current_transactions

```

# POW算法

计算下一个用来证明相连2个block关系的proof。


# hash算法

计算上一个block的json格式字符串的散列值(hash)，作为下一个block的previous_hash，用来确认相连2个block的关系。
