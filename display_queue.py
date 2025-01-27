import pymqi
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def display_queue_attributes(queue_manager_name, channel, conn_info, queue_name, attributes, mqcd=None):
    try:
        # Connect to the queue manager
        logging.info("Connecting to queue manager...")
        qmgr = pymqi.QueueManager(None)

        if mqcd:
            # Use MQCD for SSL/TLS if provided
            qmgr.connect_with_options(queue_manager_name, user="mq_user", password="mq_password", cd=mqcd)
        else:
            # Connect normally
            qmgr.connect_tcp_client(queue_manager_name, pymqi.CD(), channel, conn_info)

        logging.info(f"Connected to queue manager: {queue_manager_name}")

        # Open the queue in inquire mode
        logging.info(f"Opening queue: {queue_name}")
        queue = pymqi.Queue(qmgr, queue_name, pymqi.CMQC.MQOO_INQUIRE)

        # List of queue attributes (name and constant value)
        attributes_list = [
    ("ACCTQ"    , pymqi.CMQC.MQCA_Q_DESC),
    ("ALTTIME"  , pymqi.CMQC.MQCA_ALTERATION_TIME),
    #("BOTHRESH" , pymqi.CMQC.MQIA_BROKER_PUBQ_Q_NAMES),
    ("CLUSTER"  , pymqi.CMQC.MQCA_CLUSTER_NAME),
    #("CLWLPRTY" , pymqi.CMQC.MQIA_CLUSTER_PRIORITY),
    #("CLWLUSEQ" , pymqi.CMQC.MQIA_CLUSTER_WORKLOAD_USEQ),
    ("CRTIME"   , pymqi.CMQC.MQCA_CREATION_TIME),
    ("CUSTOM"   , pymqi.CMQC.MQCA_CUSTOM),
    ("DEFPRTY"  , pymqi.CMQC.MQIA_DEF_PRIORITY),
    ("DEFPRESP" , pymqi.CMQC.MQIA_DEF_PERSISTENCE),
    #("DEFSOPT"  , pymqi.CMQC.MQCA_DAMAGED),
    ("DESCR"    , pymqi.CMQC.MQCA_Q_DESC),
    ("GET"      , pymqi.CMQC.MQCA_Q_MGR_NAME),
    ("IMGRCOVQ" , pymqi.CMQC.MQCA_Q_NAME),
    #("IPPROCS"  , pymqi.CMQC.MQIA_IPPROCS),
    ("MAXMSGL"  , pymqi.CMQC.MQIA_MAX_MSG_LENGTH),
    #("MONQ"     , pymqi.CMQC.MQIA_MONITOR_Q),
    ("NOTRIGGER", pymqi.CMQC.MQIA_TRIGGER_CONTROL),
    #("OPPROCS"  , pymqi.CMQC.MQIA_OPPROCS),
    #("PUT"      , pymqi.CMQC.MQIA_PUT),
    ("QDEPTHHI" , pymqi.CMQC.MQIA_Q_DEPTH_HIGH_EVENT),
    ("QDPHIEV"  , pymqi.CMQC.MQIA_Q_DEPTH_HIGH_EVENT),
    ("QDPMAXEV" , pymqi.CMQC.MQIA_Q_DEPTH_MAX_EVENT),
    ("QSVCINT"  , pymqi.CMQC.MQIA_Q_DEPTH_LOW_EVENT),
    #("SCOPE"    , pymqi.CMQC.MQIA_Q_SCOPE),
    #("STATQ"    , pymqi.CMQC.MQIA_Q_STATUS),
    ("STRMQOS"  , pymqi.CMQC.MQIA_Q_SERVICE_INTERVAL),
    ("TRIGDPTH" , pymqi.CMQC.MQIA_Q_SERVICE_INTERVAL_EVENT),
    #("TRIGTYPE" , pymqi.CMQC.MQIA_Q_TRIG_TYPE),
    ("TYPE"     , pymqi.CMQC.MQIA_Q_TYPE),
    ("ALTDATE"  , pymqi.CMQC.MQCA_ALTERATION_DATE),
    ("BOQNAME"  , pymqi.CMQC.MQCA_BASE_Q_NAME),
    ("CLUSNL"   , pymqi.CMQC.MQCA_CLUSTER_NAMELIST),
    #("CLCHNAME" , pymqi.CMQC.MQCA_CHANNEL_NAME),
    #("CLWLRANK" , pymqi.CMQC.MQIA_CLUSTER_Q_MGR_PRIORITY),
    ("CRDATE"   , pymqi.CMQC.MQCA_CREATION_DATE),
    ("CURDEPTH" , pymqi.CMQC.MQIA_CURRENT_Q_DEPTH),
    ("DEFBIND"  , pymqi.CMQC.MQIA_DEF_BIND),
    ("DEFPSIST" , pymqi.CMQC.MQIA_DEF_PERSISTENCE),
    ("DEFREADA" , pymqi.CMQC.MQIA_DEF_READ_AHEAD),
    #("DEFTYPE"  , pymqi.CMQC.MQIA_DEF_TYPE),
    #("DISTL"    , pymqi.CMQC.MQIA_DIST_LIST),
    #("HARDENBO" , pymqi.CMQC.MQIA_HARDEN_BACKOUT),
    ("INITQ"    , pymqi.CMQC.MQCA_INITIATION_Q_NAME),
    ("MAXDEPTH" , pymqi.CMQC.MQIA_MAX_Q_DEPTH),
    #("MAXFSIZE" , pymqi.CMQC.MQIA_MAX_FILE_SIZE),
    ("MSGDLVSQ" , pymqi.CMQC.MQIA_MSG_DELIVERY_SEQUENCE),
    ("NPMCLASS" , pymqi.CMQC.MQIA_NPM_CLASS),
    ("PROCESS"  , pymqi.CMQC.MQCA_PROCESS_NAME),
    ("PROPCTL"  , pymqi.CMQC.MQIA_PROPERTY_CONTROL),
    ("QDEPTHLO" , pymqi.CMQC.MQIA_Q_DEPTH_LOW_EVENT),
    ("QDPLOEV"  , pymqi.CMQC.MQIA_Q_DEPTH_LOW_EVENT),
    ("QSVCIEV"  , pymqi.CMQC.MQIA_Q_SERVICE_INTERVAL_EVENT),
    ("RETINTVL" , pymqi.CMQC.MQIA_RETENTION_INTERVAL),
    ("SHARE"    , pymqi.CMQC.MQIA_SHAREABILITY),
    #("STREAMQ"  , pymqi.CMQC.MQIA_STREAM_QUEUE),
    ("TRIGDATA" , pymqi.CMQC.MQCA_TRIGGER_DATA),
    ("TRIGMPRI" , pymqi.CMQC.MQIA_TRIGGER_MSG_PRIORITY),
    ("USAGE"    , pymqi.CMQC.MQIA_USAGE)
    # Add other attributes as needed
]


        queue_attributes = [("QUEUE_NAME", queue_name)]

        for attr in attributes.upper().split():
            for attr_name, attr_constant in attributes_list:
                if attr == attr_name:
                    queue_attributes.append((attr_name, queue.inquire(attr_constant)))
                    break

        logging.info("Queue Attributes:")
        for attr, value in queue_attributes:
            logging.info(f"  {attr}: {value}")

        # Close the queue
        queue.close()
        logging.info("Queue closed.")

    except pymqi.MQMIError as e:
        logging.error(f"MQMIError: {e}")

    finally:
        # Disconnect from the queue manager
        if 'qmgr' in locals() and qmgr.is_connected:
            qmgr.disconnect()
            logging.info("Disconnected from queue manager.")

if __name__ == "__main__":
    QUEUE_MANAGER_NAME = "SKL"
    CHANNEL = "DEV.APP.SVRCONN"
    CONN_INFO = "34.207.243.99"
    USER = "mqm"
    PASSWORD = "Zaq!xsw1"
    input_data = input("")
    input_list = input_data.split()
    QUEUE_NAME = input_list[0]
    ATTRIBUTES = " ".join(input_list[1:])
    display_queue_attributes(QUEUE_MANAGER_NAME, CHANNEL, CONN_INFO, QUEUE_NAME, ATTRIBUTES)
