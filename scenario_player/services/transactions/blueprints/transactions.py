"""Send and track a transaction via JSONRPC.

The blueprint offers endpoints to send a transaction, as well
as tracking one or more transactions by their hashes.

The following endpoints are supplied by this blueprint:

    * [POST, GET] /transactions
        Request the status of one or more transactions using their hashes, or
        create a new transaction. The parameters for the latter must be supplied as
        form data.

"""
from flask import Blueprint, Response, request

from scenario_player.services.common.metrics import REDMetricsTracker
from scenario_player.services.transactions.schemas.transactions import TransactionSendRequest
from scenario_player.services.transactions.utils import get_rpc_client

transactions_blueprint = Blueprint("transactions_view", __name__)


transaction_send_schema = TransactionSendRequest()


@transactions_blueprint.route("/transactions", methods=["POST"])
def transactions_route():
    handlers = {"POST": new_transaction}
    print("Dispatching request..")
    with REDMetricsTracker(request.method, "/transactions"):
        return handlers[request.method]()


def new_transaction():
    """Create a new transaction.

    The given parameters will be passed to the service's
    :class:`raiden.network.rpc.client.JSONRPCClient` instance, which will then
    execute the transaction.

    The resulting transaction hash will be returned to the requester.

    Example::

        POST /transactions

            {
                "chain_url": <str>,
                "privkey": <str>,
                "gas_price_strategy": <str>,
                "to_address": <str>,
                "start_gas": <number>,
                "value": <number>,
            }

        200 OK

            {
                "chain_url": <str>,
                "tx_hash": <str>,
            }

    """
    data = transaction_send_schema.validate_and_deserialize(request.form)

    # Get the services JSONRPCClient from the flask app's app_context.
    chain_url, privkey = data["chain_url"], data["privkey"]
    gas_price_strategy = data["gas_price_strategy"]

    rpc_client = get_rpc_client(chain_url, privkey, gas_price_strategy)
    result = rpc_client.send_transaction(**data)

    return Response(transaction_send_schema.dumps({"tx_hash": result}).encode("UTF-8"), status=200)
