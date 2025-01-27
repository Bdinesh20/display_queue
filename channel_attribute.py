import logging
import pymqi
import sys

logging.basicConfig(level=logging.INFO)

# Define configurations
QUEUE_MANAGER_NAME = "SKL"
CONN_INFO = "34.207.243.99"
USER = "mqm"
PASSWORD = "Zaq!xsw1"

def inquire_channel(channel_name, attribute_names):
    args = {pymqi.CMQCFC.MQCACH_CHANNEL_NAME: channel_name.ljust(20).encode('utf-8')}

    qmgr = None
    try:
        qmgr = pymqi.connect(QUEUE_MANAGER_NAME, "DEV.APP.SVRCONN", CONN_INFO, USER, PASSWORD)
        pcf = pymqi.PCFExecute(qmgr)
        response = pcf.MQCMD_INQUIRE_CHANNEL(args)
    except pymqi.MQMIError as e:
        if e.comp == pymqi.CMQC.MQCC_FAILED:
            logging.error(f'MQ Error: Comp Code: {e.comp}, Reason Code: {e.reason}')
            if e.reason == pymqi.CMQC.MQRC_CHANNEL_CONFIG_ERROR:
                logging.error(f'Channel configuration error for channel: {channel_name}. Please verify the channel definition and its configuration.')
            elif e.reason == pymqi.CMQC.MQRC_UNKNOWN_OBJECT_NAME:
                logging.error(f'No channel found with name: {channel_name}')
        else:
            raise
    else:
        attribute_map = {
           #"ALTDATE": pymqi.CMQCFC.MQCACH_ALT_DATE,
            #"ALTTIME": pymqi.CMQCFC.MQCACH_ALT_TIME,
            "BATCHSZ": pymqi.CMQCFC.MQIACH_BATCH_SIZE,
            #"CERTLABL": pymqi.CMQCFC.MQCACH_CERT_LABEL,
            #"COMPHDR": pymqi.CMQCFC.MQIACH_COMPRESSION_HDR,
            #"COMPMSG": pymqi.CMQCFC.MQIACH_COMPRESSION,
            "DESCR": pymqi.CMQCFC.MQCACH_DESC,
            "HBINT": pymqi.CMQCFC.MQIACH_KEEP_ALIVE_INTERVAL,
            "KAINT": pymqi.CMQCFC.MQIACH_KEEP_ALIVE_INTERVAL,
            "MAXMSGL": pymqi.CMQCFC.MQIACH_MAX_MSG_LENGTH,
            "MCAUSER": pymqi.CMQCFC.MQCACH_MCA_USER_ID,
            #"MONCHL": pymqi.CMQCFC.MQIACH_MONITORING_CHANNEL,
            #"MRDATA": pymqi.CMQCFC.MQCACH_MR_DATA,
            "MREXIT": pymqi.CMQCFC.MQCACH_MSG_EXIT_NAME,
            #"MRRTY": pymqi.CMQCFC.MQIACH_MSG_RETRY_COUNT,
            #"MRTMR": pymqi.CMQCFC.MQIACH_MSG_EXIT_RESPONSE,
            #"MSGDATA": pymqi.CMQCFC.MQCACH_MSG_DATA,
            "MSGEXIT": pymqi.CMQCFC.MQCACH_MSG_EXIT_NAME,
            "NPMSPEED": pymqi.CMQCFC.MQIACH_NPM_SPEED,
            "PUTAUT": pymqi.CMQCFC.MQIACH_PUT_AUTHORITY,
            #"RCVDATA": pymqi.CMQCFC.MQCACH_RCV_DATA,
            "RCVEXIT": pymqi.CMQCFC.MQCACH_RCV_EXIT_NAME,
            "RESETSEQ": pymqi.CMQCFC.MQIACH_RESET_REQUESTED,
            #"SCYDATA": pymqi.CMQCFC.MQCACH_SEC_DATA,
            "SCYEXIT": pymqi.CMQCFC.MQCACH_SEC_EXIT_NAME,
            #"SENDDATA": pymqi.CMQCFC.MQCACH_SEND_DATA,
            "SENDEXIT": pymqi.CMQCFC.MQCACH_SEND_EXIT_NAME,
            #"SEQWRAP": pymqi.CMQCFC.MQIACH_SEQUENCE_WRAP,
            "SSLCAUTH": pymqi.CMQCFC.MQIACH_SSL_CLIENT_AUTH,
            "SSLCIPH": pymqi.CMQCFC.MQCACH_SSL_CIPHER_SPEC,
            "SSLPEER": pymqi.CMQCFC.MQCACH_SSL_PEER_NAME,
            "STATCHL": pymqi.CMQCFC.MQIACH_CHANNEL_STATUS,
            "TRPTYPE": pymqi.CMQCFC.MQIACH_XMIT_PROTOCOL_TYPE,
            #"USEDLQ": pymqi.CMQCFC.MQIACH_USE_DEAD_LETTER_Q,
            "DISCINT": pymqi.CMQCFC.MQIACH_DISC_INTERVAL,
            "MAXINST": pymqi.CMQCFC.MQIACH_MAX_INSTANCES,
            #"MAXINSTC": pymqi.CMQCFC.MQIACH_MAX_INSTC,
            #"SHARECNV": pymqi.CMQCFC.MQIACH_SHARECNV,
            #"BATCHHB": pymqi.CMQCFC.MQIACH_BATCH_HEARTBEAT,
            "BATCHINT": pymqi.CMQCFC.MQIACH_BATCH_INTERVAL,
            #"BATCHLIM": pymqi.CMQCFC.MQIACH_BATCH_SIZE_LIMIT,
            "CONNAME": pymqi.CMQCFC.MQCACH_CONNECTION_NAME,
            #"CONVERT": pymqi.CMQCFC.MQIACH_CONVERT_MSG,
            "LOCLADDR": pymqi.CMQCFC.MQCACH_LOCAL_ADDRESS,
            "LONGRTY": pymqi.CMQCFC.MQIACH_LONG_RETRY,
            "LONGTMR": pymqi.CMQCFC.MQIACH_LONG_TIMER,
            "MCANAME": pymqi.CMQCFC.MQCACH_MCA_NAME,
            "MCATYPE": pymqi.CMQCFC.MQIACH_CHANNEL_TYPE,
            "MODENAME": pymqi.CMQCFC.MQCACH_MODE_NAME,
            "PASSWORD": pymqi.CMQCFC.MQCACH_PASSWORD,
            #"PROPCTL": pymqi.CMQCFC.MQIACH_PROPERTY_CONTROL,
            "SHORTRTY": pymqi.CMQCFC.MQIACH_SHORT_RETRY,
            "SHORTTMR": pymqi.CMQCFC.MQIACH_SHORT_TIMER,
            "TPNAME": pymqi.CMQCFC.MQCACH_TP_NAME,
            "USERID": pymqi.CMQCFC.MQCACH_USER_ID,
            "XMITQ": pymqi.CMQCFC.MQCACH_XMIT_Q_NAME,
            "AMQPKA": pymqi.CMQCFC.MQIACH_KEEP_ALIVE_INTERVAL,
            "PORT": pymqi.CMQCFC.MQIACH_PORT_NUMBER,
            "TPROOT": pymqi.CMQCFC.MQCACH_TOPIC_ROOT,
            #"TMPMODEL": pymqi.CMQCFC.MQCACH_TEMP_MODEL_Q,
            #"TMPQPRFX": pymqi.CMQCFC.MQCACH_TEMP_Q_PREFIX,
            "USECLTID": pymqi.CMQCFC.MQIACH_USE_CLIENT_ID,
            #"CLUSNL": pymqi.CMQCFC.MQCACH_CLUS_CHL_NAME,
            #"CLUSTER": pymqi.CMQCFC.MQCACH_CLUSTER_NAME,
            #"CLWLPRTY": pymqi.CMQCFC.MQIACH_CLUS_CHL_PRIORITY,
            #"CLWLRANK": pymqi.CMQCFC.MQIACH_CLUS_CHL_RANK,
            #"CLWLWGHT": pymqi.CMQCFC.MQIACH_CLUS_CHL_WEIGHT,
            "NETPRTY": pymqi.CMQCFC.MQIACH_NETWORK_PRIORITY,
            "AFFINITY": pymqi.CMQCFC.MQIACH_CHANNEL_TYPE,
            "DEFRECON": pymqi.CMQCFC.MQIACH_DEF_RECONNECT,
            #"QMNAME": pymqi.CMQCFC.MQCACH_Q_MGR_NAME,
        }

        for attribute_name in attribute_names:
            attribute_key = attribute_map.get(attribute_name)
            if attribute_key:
                attribute_value = response[0].get(attribute_key, None)
                if attribute_value is not None:
                    if isinstance(attribute_value, bytes):
                        attribute_value = attribute_value.decode('utf-8').strip()
                    logging.info(f"{attribute_name}: {attribute_value}")
                else:
                    logging.info(f"Attribute '{attribute_name}' not found for channel '{channel_name}'")
            else:
                logging.info(f"Invalid attribute name: {attribute_name}")
    finally:
        if qmgr:
            qmgr.disconnect()

if __name__ == "__main__":
    user_input = input("Enter the channel name and attribute names separated by spaces: ")
    inputs = user_input.split()
    channel_name = inputs[0]
    attribute_names = inputs[1:]
    inquire_channel(channel_name, attribute_names)
