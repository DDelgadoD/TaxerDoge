import asyncio
import logging
import json

from Database import Movements, Transactions, session, max_id
from ExternalAPI import base_get


def json_import(filename):
    if filename:
        with open(filename, 'r') as f:
            js = json.load(f)
    else:
        raise Exception
    return js


async def detail_tx(tx_id):
    data = await base_get(ep["api_url"] + ep["TX"] + ep["NET"], "/" + tx_id)
    return data


def add_mov(data):
    mov = Movements(status=data['status'], network=data['data']['network'], address=data['data']['address'])
    session.add(mov)
    session.commit()
    return mov


def add_tx(txs, mov):
    for tx in txs:
        tx["mov_id"] = mov.id
        detail_tx(tx["tx_id"])
    session.bulk_insert_mappings(Transactions, txs)
    session.commit()


async def movements():
    logging.info(m["m_log"]["Start"])
    max_tx = max_id(Transactions.time, Transactions.txid)
    for key, value in ep["addresses"].items():
        for path in [ep["TX_UNSPENT"], ep["TX_SPENT"], ep["TX_RECEIVED"]]:
            data = await base_get(ep["api_url"] + path + ep["NET"], value + max_tx)
            txs = data["data"]["txs"]
            if txs:
                mov = add_mov(data)
                logging.info(m["m_log"]["Addedmov"])
                add_tx(txs, mov)
                logging.info(m["m_log"]["Addedtx"])
    logging.info(m["m_log"]["End"])


if __name__ == "__main__":
    var = json_import("vars.json")
    m = var["messages"]
    ep = var["endpoints"]

    logging.basicConfig(filename=m["log_path"], filemode='a',
                        format='%(asctime)s %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(movements())
    session.close()
