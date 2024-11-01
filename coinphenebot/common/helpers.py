def parse_wallet_balances(tokens):
    result = {}
    if len(tokens["tokens"]) == 0:
                return result
    elif len(tokens["tokens"]) == 1:
        if tokens["tokens"][0]["symbol"] == "SOL":
            bal = tokens["tokens"][0]
            result["SOL"] = {
                "name": bal["name"],
                "symbol": bal["symbol"],
                "amount": bal["totalUiAmount"],
                "address": bal["mint"],
                "price": bal["price"] if bal ["price"] else None,
                "sol_price": bal["solPrice"] if bal ["solPrice"] else None
            }
            return result

    for bal in tokens["tokens"]:
        name = bal["name"]
        result[name] = {
            "name": bal["name"],
            "symbol": bal["symbol"],
            "amount": bal["totalUiAmount"],
            "address": bal["mint"],
            "price": bal["price"] if "price" in bal else None,
            "sol_price": bal["solPrice"] if bal ["solPrice"] else None
        }
    
    return result


def parse_sol_balance(tokens):
    if tokens["tokens"][0]["symbol"] == "SOL":
            return tokens["tokens"][0]["totalUiAmount"]
    
    iterator = filter(lambda x: x["symbol"] == "SOL", tokens["tokens"])
    sol_token = [x for x in iterator]
    return sol_token[0]["totalUiAmount"]