# -*- coding: utf-8 -*-
'''blockchain rpc related functions'''

import jsonrpclib

DEFAULT_HOSTNAME = 'localhost'
DEFAULT_PORT = 8332
DEFAULT_SCHEMA = 'http'



def make_server_from_url(url):
    '''Return a `jsonrpclib.Server` instance initialized with the given url'''
    return jsonrpclib.Server(url)


def make_server_url(username, password, hostname=DEFAULT_PORT, port=DEFAULT_PORT, schema=DEFAULT_SCHEMA):
    return '{schema}://{username}:{password}@{hostname}:{port}'.format(schema=schema,
                                                                       username=username,
                                                                       password=password,
                                                                       hostname=hostname,
                                                                       port=port)


def make_server(username, password, hostname=DEFAULT_HOSTNAME, port=DEFAULT_PORT, schema=DEFAULT_SCHEMA):
    return make_server_from_url(make_server_url(username=username,
                                                password=password,
                                                hostname=hostname,
                                                port=port,
                                                schema=schema))

def get_block_height(SERVER):
    return SERVER.getblockcount()

def get_block_transactions(blockindex, SERVER):
    """
    Gets transaction data from block ranges
    """
    txlist = []
    blockhash = SERVER.getblockhash(blockindex)  # Gets the block hash from the block index number
    for tx in SERVER.getblock(blockhash)['tx']:  # Gets all transactions from block hash
        txlist += [tx]
    return txlist

def get_data_local(transaction, SERVER):
    """
    Downloads data from Bitcoin Core RPC and returns hex
    """
    
    rawTx = SERVER.getrawtransaction(transaction)   # gets the raw transaction from RPC
    tx = SERVER.decoderawtransaction(rawTx)         # Decodes the raw transaction from RPC
    hexdata = ''
    for txout in tx['vout']:
        for op in txout['scriptPubKey']['asm'].split(' '):  # searches for all OP data
            if not op.startswith('OP_') and len(op) >= 40:
                hexdata += op.encode('utf8')
    return hexdata

def get_indata_local(transaction, SERVER)                                             :
    rawTx = SERVER.getrawtransaction(transaction)   # gets the raw transaction from RPC
    tx = SERVER.decoderawtransaction(rawTx)         # Decodes the raw transaction from RPC
    inhex = ''
    for txin in tx['vin']:
        try:
            for inop in txin['scriptSig']['hex'].split():  # Gathers the input script
                inhex += inop
        except KeyError:
            inhex += ''
    return inhex