import math
import logging
from typing import Any, Dict, Type
from .helper import GetAoneTokenInfo, GetExchangeAndSegment
from SmartApi.smartConnect import SmartConnect

logger = logging.getLogger(__name__)

class BrokerBase:
    """
    Base class for all brokers that defines a common interface for broker operations.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def buy(self, order_type: str, quantity: int) -> None:
        """
        Abstract method to handle buying stocks.
        Must be implemented by subclasses.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")

    def sell(self, order_type: str, price: float, quantity: int) -> None:
        """
        Abstract method to handle selling stocks.
        Must be implemented by subclasses.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")
    
    def prepare_order_parms(self, symbol, transactiontype, order_type, price, tgt, sl, qty):
        """
        Abstract method to prepare order parameters.
        Must be implemented by subclasses.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")
        

class AngelOne(BrokerBase):
    """
    Specific implementation for AngelOne.
    """
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.config = config

        self.obj=SmartConnect(
            api_key=config["api_key"], 
            access_token=config["access_token"],
            refresh_token=config["refresh_token"],
            feed_token=config["feed_token"],
            userId=config["userId"]
        )

    def buy(self, symbol: str, strick_price: int, cepe: str, order_type: str, price: float, quantity: int, tgt: float, sl: float) -> None:

        legs = quantity/900

        LowerCounter = math.floor(legs)
        UpperCounter = math.ceil(legs)

        while UpperCounter > 0:

            if UpperCounter == 1:
                QTY_TO_BUY = quantity - (900*LowerCounter)
            else:
                QTY_TO_BUY = 900
            
            order_params = self.prepare_order_parms(symbol, 'BUY', cepe, strick_price, order_type, price, tgt, sl, QTY_TO_BUY)
            UpperCounter = UpperCounter - 1
            orderid = self.obj.placeOrder(order_params)
            logger.info(f"Buying with AngelOne: OrderID:{orderid}, Quantity:{quantity}")


    def sell(self, symbol: str, strick_price: int, cepe: str, order_type: str, price: float, quantity: int, tgt: float, sl: float) -> None:
        legs = quantity/900

        LowerCounter = math.floor(legs)
        UpperCounter = math.ceil(legs)

        while UpperCounter > 0:

            if UpperCounter == 1:
                QTY_TO_SELL = quantity - (900*LowerCounter)
            else:
                QTY_TO_SELL = 900
            
            order_params = self.prepare_order_parms(symbol, 'SELL', cepe, strick_price, order_type, price, tgt, sl, QTY_TO_SELL)
            UpperCounter = UpperCounter - 1
            orderid = self.obj.placeOrder(order_params)
            logger.info(f"Selling with AngelOne OrderID:{orderid}, Quantity:{quantity}")
    
    def prepare_order_parms(self, symbol, transactiontype, cepe, strick_price, order_type, price, tgt, sl, qty):
        
        TokenInfo = GetAoneTokenInfo(symbol, cepe, strick_price).iloc[0]
        full_symbol = TokenInfo["symbol"]
        symbol_token = TokenInfo["token"]

        exchange = GetExchangeAndSegment(symbol)[0]

        orderparams = {
            "variety": "NORMAL",
            "tradingsymbol": full_symbol,
            "symboltoken": symbol_token,
            "transactiontype": transactiontype,
            "exchange": exchange,
            "ordertype": order_type,
            "producttype": "INTRADAY",
            "duration": "DAY",
            "price": price,
            "squareoff": tgt,
            "stoploss": sl,
            "quantity": qty
        }

        return orderparams


class BrokerClient:
    """
    Main class to interact with brokers. Handles broker instantiation and delegates method calls.
    """
    def __init__(self, broker_name: str, config: Dict[str, Any]):
        self.broker = self._get_broker(broker_name, config)

    def _get_broker(self, broker_name: str, config: Dict[str, Any]) -> BrokerBase:
        brokers: Dict[str, Type[BrokerBase]] = {
            "aone": AngelOne,
        }
        broker_class = brokers.get(broker_name.lower())
        if not broker_class:
            logger.error(f"Broker not found: {broker_name}")
            raise ValueError("Broker not found")
        return broker_class(config)

    def buy(self, symbol: str, strick_price: int, cepe: str, order_type: str, price: float, quantity: int, tgt: float, sl: float) -> None:
        self.broker.buy(symbol, strick_price, cepe, order_type, price, quantity, tgt, sl)

    def sell(self, symbol: str, strick_price: int, cepe: str, order_type: str, price: float, quantity: int, tgt: float, sl: float) -> None:
        self.broker.sell(symbol, strick_price, cepe, order_type, price, quantity, tgt, sl)
