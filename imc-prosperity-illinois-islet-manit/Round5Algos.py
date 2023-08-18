from typing import Any, Dict, List
from datamodel import OrderDepth, TradingState, Order, ProsperityEncoder, Symbol
import json

class Logger:
    def __init__(self) -> None:
        self.logs = ""

    def print(self, *objects: Any, sep: str = " ", end: str = "\n") -> None:
        self.logs += sep.join(map(str, objects)) + end

    def flush(self, state: TradingState, orders: dict[Symbol, list[Order]]) -> None:
        print(json.dumps({
            "state": state,
            "orders": orders,
            "logs": self.logs,
        }, cls=ProsperityEncoder, separators=(",", ":"), sort_keys=True))

        self.logs = ""

logger = Logger()


class Trader:
    global temp
    # moving average array for bananas
    temp = []
    # global momentum
    # global prices
    # #momentum array for diving gear
    # prices = []
    # momentum = []
    global dolphinSMA
    dolphinSMA = []
    count = 0
    def run(self, state: TradingState) -> Dict[str, List[Order]]:

        def amount_to_get_to_position(desired_position, product):
            curr_position = state.position.get(product, 0)
            return desired_position - curr_position
                

        """
        Only method required. It takes all buy and sell orders for all symbols as an input,
        and outputs a list of orders to be sent
        """
        # Initialize the method output dict as an empty dict
        result = {}
        # Iterate over all the keys (the available products) contained in the order dephts
        for product in state.order_depths.keys():

            # Check if the current product is the 'PEARLS' product, only then run the order logic
            if product == 'PEARLS':

                # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
                order_depth: OrderDepth = state.order_depths[product]

                # Initialize the list of Orders to be sent as an empty list
                orders: list[Order] = []

                # Define a fair value for the PEARLS.
                # Note that this value of 1 is just a dummy value, you should likely change it!
                acceptable_price = 10000

                # If statement checks if there are any SELL orders in the PEARLS market
                if len(order_depth.sell_orders) > 0:

                    # Sort all the available sell orders by their price,
                    # and select only the sell order with the lowest price
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]

                    # Check if the lowest ask (sell order) is lower than the above defined fair value
                    #if best_ask < acceptable_price:
                    for best_ask, best_ask_volume in order_depth.sell_orders.items():
                        if best_ask < 10002:
                        # In case the lowest ask is lower than our fair value,
                        # This presents an opportunity for us to buy cheaply
                        # The code below therefore sends a BUY order at the price level of the ask,
                        # with the same quantity
                        # We expect this order to trade with the sell order
                            print("BUY", str(-best_ask_volume) + "x", best_ask)
                            orders.append(Order(product, best_ask, -best_ask_volume))

                # The below code block is similar to the one above,
                # the difference is that it find the highest bid (buy order)
                # If the price of the order is higher than the fair value
                # This is an opportunity to sell at a premium
                if len(order_depth.buy_orders) != 0:
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    for best_bid, best_bid_volume in order_depth.buy_orders.items():
                        if best_bid > 9998:
                            print("SELL", str(best_bid_volume) + "x", best_bid)
                            orders.append(Order(product, best_bid, -best_bid_volume))

                # if product in state.market_trades:
                #     market_order_depth = state.market_trades[product]
                #     for i in market_order_depth:
                #         if i.buyer == 'Gary' and i.price > 10001:
                #             orders.append(Order(product, i.price, i.quantity))
                #         if i.seller == 'Gary' and i.price < 9999:
                #             orders.append(Order(product, i.price, i.quantity))
                #         if i.buyer == 'Penelope' and i.price > 10001:
                #             orders.append(Order(product, i.price, i.quantity))
                #         if i.seller == 'Penelope' and i.price < 9999:
                #             orders.append(Order(product, i.price, i.quantity))

                # Add all the above the orders to the result dict
                result[product] = orders


            # --------------------------------------------------------------------------------------------------------------------


            # Check if the current product is the 'BANANAS' product, only then run the order logic
            if product == 'BANANAS':

                # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
                order_depth: OrderDepth = state.order_depths[product]

                # Initialize the list of Orders to be sent as an empty list
                orders: list[Order] = []
                
                best_bid = 0
                best_ask = 0
                if len(order_depth.sell_orders) > 0:
                    best_ask = min(order_depth.sell_orders.keys())
                if len(order_depth.buy_orders) != 0:
                    best_bid = max(order_depth.buy_orders.keys())
                    if (best_ask == 0):
                        best_ask = best_bid
                else:
                    best_bid = best_ask

                # Don't do anything if order book is empty
                if best_bid == 0 and best_ask == 0:
                    break

                # Now update our list
                if(len(temp) == 13):
                    temp.pop(0)
                temp.append((best_ask + best_bid)/2)

                # Try a mean reversion thing
                fair_price = sum(temp) / len(temp)

                # If statement checks if there are any SELL orders in the BANANAS market
                if len(order_depth.sell_orders) > 0:
                    best_ask_volume = order_depth.sell_orders[best_ask]

                    # Look at moving averages
                    if len(temp) > 1 and best_ask < fair_price:
                        # Send buy order
                        print("BUY", str(-best_ask_volume) + "x", best_ask)
                        orders.append(Order(product, best_ask, -best_ask_volume))


                # I think here we should mirror the if statement above, for selling?
                # If statement checks if there are any BUY orders in the BANANAS market
                if len(order_depth.buy_orders) > 0:
                    best_bid_volume = order_depth.buy_orders[best_bid]

                    # Look at moving averages
                    if len(temp) > 1 and best_bid > fair_price:
                        # Send sell order
                        print("SELL", str(best_bid_volume) + "x", best_bid)
                        orders.append(Order(product, best_bid, -best_bid_volume))
                        
                if product in state.market_trades:
                    market_order_depth = state.market_trades[product]
                    for i in market_order_depth:
                        if i.buyer == 'Olivia':
                            orders.append(Order(product, i.price, i.quantity))
                        if i.seller == 'Olivia':
                            orders.append(Order(product, i.price, -i.quantity))
                        if i.buyer == 'Pablo':
                            orders.append(Order(product, i.price, -i.quantity))
                        if i.seller == 'Pablo':     #if pablo's selling, we should buy cuz he doesn't know what he's doing
                            orders.append(Order(product, i.price, i.quantity))
                        if i.buyer == 'Charlie':
                            orders.append(Order(product, i.price, i.quantity))
                        if i.seller == 'Charlie':
                            orders.append(Order(product, i.price, -i.quantity))

                # Add all the above the orders to the result dict
                result[product] = orders
                # Return the dict of orders
                # These possibly contain buy or sell orders for PEARLS
                # Depending on the logic above



            # --------------------------------------------------------------------------------------------------------------------



            # Only check for coconuts, so that we don't go through this twice
            if product == 'COCONUTS':
                # Retrieve the Order Depth containing all the market BUY and SELL orders, for both coconuts and pina coladas
                coconut_order_depth: OrderDepth = state.order_depths['COCONUTS']
                pina_colada_order_depth: OrderDepth = state.order_depths['PINA_COLADAS']
                # Initialize the list of Orders to be sent as an empty list
                # Let's use two orders lists
                coconut_orders: list[Order] = []
                pina_colada_orders: list[Order] = []

                # pairs trading
                fair_ratio = 15 / 8
                # From Day -1
                one_std = 0.0037252314674358217
                # Want to linearly scale our position
                max_ratio = 1.8804199279413591
                min_ratio = 1.8636729637658718

                # If statement checks if there are any SELL and BUY orders for coconuts
                coconut_best_ask = None
                coconut_best_bid = None
                coconut_best_ask_volume = None
                coconut_best_bid_volume = None
                if len(coconut_order_depth.sell_orders) > 0:
                    coconut_best_ask = min(coconut_order_depth.sell_orders.keys())
                    coconut_best_ask_volume = coconut_order_depth.sell_orders[coconut_best_ask]
                if len(coconut_order_depth.buy_orders) > 0:
                    coconut_best_bid = max(coconut_order_depth.buy_orders.keys())
                    coconut_best_bid_volume = coconut_order_depth.buy_orders[coconut_best_bid]

                # If statement checks if there are any SELL and BUY orders for pina_coladas
                pina_colada_best_ask = None
                pina_colada_best_bid = None
                pina_colada_best_ask_volume = None
                pina_colada_best_bid_volume = None
                if len(pina_colada_order_depth.sell_orders) > 0:
                    pina_colada_best_ask = min(pina_colada_order_depth.sell_orders.keys())
                    pina_colada_best_ask_volume = pina_colada_order_depth.sell_orders[pina_colada_best_ask]
                if len(pina_colada_order_depth.buy_orders) > 0:
                    pina_colada_best_bid = max(pina_colada_order_depth.buy_orders.keys())
                    pina_colada_best_bid_volume = pina_colada_order_depth.buy_orders[pina_colada_best_bid]

                # Only send orders if we can even calculate a current ratio
                if (coconut_best_ask is not None and coconut_best_bid is not None 
                    and pina_colada_best_ask is not None and pina_colada_best_bid is not None):
                    coconut_mid_price = (coconut_best_ask + coconut_best_bid) / 2
                    pina_colada_mid_price = (pina_colada_best_ask + pina_colada_best_bid) / 2
                    current_ratio = pina_colada_mid_price / coconut_mid_price

                    current_ratio_linear_scale = (current_ratio - min_ratio) / (max_ratio - min_ratio)

                    desired_coconut_position = (current_ratio_linear_scale * (-600)) + 300
                    desired_pina_colada_position = (current_ratio_linear_scale * 1200) - 600

                    # Ok so now we've figured out the positions we want for coconuts and pina coladas
                    # Now we just need to send orders so that we can get to those positions
                    # cool_function(desired_coconut_position, desired_pina_colada_position)

                    pina_colada_order_volume = amount_to_get_to_position(desired_pina_colada_position, 'PINA_COLADAS')

                    if current_ratio < (15/8 - (one_std/3)):            #sell coconuts
                        

                        print("SELL", str(coconut_best_bid_volume) + "x", coconut_best_bid)
                        coconut_orders.append(Order('COCONUTS', coconut_best_bid, -coconut_best_bid_volume))
                        # coconut_orders.append(Order('COCONUTS', coconut_best_bid, -15))
                        # coconut_orders.append(Order('COCONUTS', coconut_best_bid, -(pina_colada_order_volume * (8 / 15))))

                        print("BUY", str(-pina_colada_best_ask_volume) + "x", pina_colada_best_ask)
                        pina_colada_orders.append(Order('PINA_COLADAS', pina_colada_best_ask, -pina_colada_best_ask_volume))
                        # pina_colada_orders.append(Order('PINA_COLADAS', pina_colada_best_ask, 8))
                        # pina_colada_orders.append(Order('PINA_COLADAS', pina_colada_best_ask, pina_colada_order_volume))

                    if current_ratio > (15/8 + (one_std/3)):
                        coconut_orders.append(
                            Order('COCONUTS', coconut_best_ask, -coconut_best_ask_volume))
                        # coconut_orders.append(
                        #     Order('COCONUTS', coconut_best_ask, 15))
                        # coconut_orders.append(
                        #     Order('COCONUTS', coconut_best_ask, -(pina_colada_order_volume * (8 / 15))))
                        
                        pina_colada_orders.append(
                            Order('PINA_COLADAS', pina_colada_best_bid, -pina_colada_best_bid_volume))
                        # pina_colada_orders.append(
                        #     Order('PINA_COLADAS', pina_colada_best_bid, -8))
                        # pina_colada_orders.append(
                        #     Order('PINA_COLADAS', pina_colada_best_bid, pina_colada_order_volume))

                    result['COCONUTS'] = coconut_orders
                    result['PINA_COLADAS'] = pina_colada_orders

    # --------------------------------------------------------------------------------------------------------------------
            if product == 'BERRIES':

                # Retrieve the Order Depth containing all the market BUY and SELL orders for BERRIES
                order_depth: OrderDepth = state.order_depths[product]

                # Initialize the list of Orders to be sent as an empty list
                orders: list[Order] = []

                # Define a fair value for the BERRIES.
                # Note that this value of 1 is just a dummy value, you should likely change it!
                acceptable_price = 10000

                # If statement checks if there are any SELL orders in the BERRIES market
                if len(order_depth.sell_orders) > 0:

                    # Sort all the available sell orders by their price,
                    # and select only the sell order with the lowest price
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]
                    if (state.timestamp > (0.2 * 10**6)) and (state.timestamp < (0.4 * 10**6)):
                        orders.append(Order('BERRIES', best_ask, -best_ask_volume))

                # The below code block is similar to the one above,
                # the difference is that it find the highest bid (buy order)
                # If the price of the order is higher than the fair value
                # This is an opportunity to sell at a premium
                if len(order_depth.buy_orders) != 0:
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    if (state.timestamp > (0.5 * 10**6)) and (state.timestamp < (0.8 * 10**6)):
                        orders.append(Order('BERRIES', best_bid, -best_bid_volume))
                if product in state.market_trades:
                    market_order_depth = state.market_trades[product]
                    for i in market_order_depth:
                        if i.buyer == 'Olivia':
                            orders.append(Order(product, i.price, i.quantity))
                        if i.seller == 'Olivia':
                            orders.append(Order(product, i.price, -i.quantity))
                        if i.buyer == 'Gina':
                            orders.append(Order(product, i.price, i.quantity))
                        if i.seller == 'Gina':
                            orders.append(Order(product, i.price, -i.quantity))
                # Add all the above the orders to the result dict
                result[product] = orders
#---------------------------------------------------------------------------------------------------------------------------------------
            if product == 'UKULELE':
                if product in state.market_trades:
                    market_order_depth = state.market_trades[product]
                    for i in market_order_depth:
                        if i.buyer == 'Olivia':
                            orders.append(Order(product, i.price, i.quantity))
                        if i.seller == 'Olivia':
                            orders.append(Order(product, i.price, -i.quantity))
                result[product] = orders

            if product == 'PICNIC_BASKET':
                # basket_order_depth: OrderDepth = state.order_depths['PICNIC_BASKET']
                # dip_order_depth: OrderDepth = state.order_depths['DIP']
                # baguette_order_depth: OrderDepth = state.order_depths['BAGUETTE']
                # ukulele_order_depth: OrderDepth = state.order_depths['UKULELE']
                
                basket_orders: list[Order] = []
                dip_orders: list[Order] = []
                baguette_orders: list[Order] = []
                ukulele_orders: list[Order] = []
                
                # not set in stone, only for day 1 so far, basket - items summed
                mean_delta = 376
                std_delta = 120
                
                def getBestAsk(instrument):
                    if len(state.order_depths[instrument].sell_orders) > 0:
                        return min(state.order_depths[instrument].sell_orders.keys())
                    else:
                        return 0
                    
                def getBestBid(instrument):
                    if len(state.order_depths[instrument].buy_orders) > 0:
                        return max(state.order_depths[instrument].buy_orders.keys())
                    else:
                        return 0
                    
                bb_basket = getBestBid('PICNIC_BASKET')
                ba_basket = getBestAsk('PICNIC_BASKET')
                mp_basket = (ba_basket + bb_basket)/2
                
                bb_dip = getBestBid('DIP')
                ba_dip = getBestAsk('DIP')
                mp_dip = (bb_dip + ba_dip)/2
                bb_baguette = getBestBid('BAGUETTE')
                ba_baguette = getBestAsk('BAGUETTE')
                mp_baguette = (bb_baguette + ba_baguette)/2
                bb_ukulele = getBestBid('UKULELE')
                ba_ukulele = getBestAsk('UKULELE')
                mp_ukulele = (bb_ukulele + ba_ukulele)/2
                
                rough_sum = mp_dip*4 + mp_baguette*2 + mp_ukulele
                
                if all(var != 0 for var in [bb_basket, ba_basket, bb_dip, ba_dip, bb_baguette, ba_baguette, bb_ukulele, ba_ukulele]):
                    # probably want to add some form of threshold like on the last pairs algo, in this case I used 1 std
                    # the signs might be fucked up and so is the ><, need to fix
                    if mp_basket - rough_sum > (mean_delta + std_delta*2):
                        # sell baskets, buy items
                        basket_orders.append(Order('PICNIC_BASKET', bb_basket, -1))
                        dip_orders.append(Order('DIP', ba_dip, 4))
                        baguette_orders.append(Order('BAGUETTE', ba_baguette, 2))
                        ukulele_orders.append(Order('UKULELE', ba_ukulele, 1))

                    if mp_basket - rough_sum < (mean_delta - std_delta*2):
                        # buy baskets sell items
                        basket_orders.append(Order('PICNIC_BASKET', ba_basket, 1))
                        dip_orders.append(Order('DIP', bb_dip, -4))
                        baguette_orders.append(Order('BAGUETTE', bb_baguette, -2))
                        ukulele_orders.append(Order('UKULELE', bb_ukulele, -1))
                        
                    result['PICNIC_BASKET'] = basket_orders
                    result['DIP'] = dip_orders
                    result['BAGUETTE'] = baguette_orders
                    result['UKULELE'] = ukulele_orders
                    
        logger.flush(state, result)
        return result
