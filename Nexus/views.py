from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .brokers import BrokerClient


class BrokerPlaceOrder(APIView):
    def post(self, request, broker_code):
        try:
            broker_config = request.data.get('broker_config', {}) 
            broker_client = BrokerClient(broker_code, broker_config)

            symbol = request.data.get('symbol')
            strick_price = request.data.get('strick_price')
            cepe = request.data.get('cepe')
            order_type = request.data.get('order_type')
            price = request.data.get('price')
            quantity = request.data.get('quantity')
            tgt = request.data.get('tgt')
            sl = request.data.get('sl')

            if request.data.get('action') == 'buy':
                broker_client.buy(symbol, strick_price, cepe, order_type, price, quantity, tgt, sl)
            elif request.data.get('action') == 'sell':
                broker_client.sell(symbol, strick_price, cepe, order_type, price, quantity, tgt, sl)
            else:
                return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": "Order placed successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
