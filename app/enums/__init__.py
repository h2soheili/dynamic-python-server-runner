from enum import Enum


class KafkaTopics(Enum):
    OrderExecution = 'ir.mofid.sub.order.execution'
    MarketData = 'ir.mofid.sub.market.data'


class TableNames(Enum):
    OrderTable = 'Order'
    TickerTable = 'Ticker'
    ProcessTable = 'Process'
    ProcessTickerTable = 'ProcessTicker'


class EventTypes(Enum):
    ReProcess = 'ir.mofid.reprocess'


class ClusterKey(str, Enum):
    CryptoTop = 'crypto.top'
    IranTop = 'iran.top'
