"""
Functions used in lab5
"""

import network                                              # import network module

ESSID = 'SpectrumSetup-20'                                  # define network credentials
PWD = 'violetwhale387'
#PWD = 'coolbrain145'

def connect(returnIP=False):
    """
    Connects the esp8266 to wifi network
    """
    print("Connecting to WiFi...")
    router_connection = network.WLAN(network.STA_IF)        # construct connection object
    router_connection.active(True)                          # activate connection
    #router_connection.disconnect()
    router_connection.connect(ESSID, PWD)                   # specify credentials
    IP = router_connection.ifconfig()[0]                    # get IP address
    print("Connected to {} as {}".format(ESSID, IP))        # display for confirmation
    if returnIP:
        return IP

def date_builder(datetime_tuple, beat, position, mode, alarming=False):
    """
    Function for building date structures

    params:
        datetime_tuple: tuple of datetime values. Length 8 except for alarming
                        case which is length 3

        beat: the iteration variable, if beat is divisible by 5, we have the
              current value appear to blink. Used to indicate the position
              for changing time and setting alarms

        position: the current position in the date string

        mode: the display state of the Watch

        alarming: boolean specifying if an alarm was triggered.
    """
    if alarming:                    # if alarming, return date string
        if beat%5 == 0:             # except when beat is divisible by 5, this
            return ""               # causes the alarm time to blink
        else:
            date_string = "{}:{}:{}".format(datetime_tuple[0],
                                            datetime_tuple[1],
                                            datetime_tuple[2])
    elif (mode > 0) and (beat%5 == 0):  # if changing time of setting alarm, blink current position.
        if position == 4:
            date_string = "  :{}:{}".format(datetime_tuple[5],
                                            datetime_tuple[6])
        elif position == 5:
            date_string = "{}:  :{}".format(datetime_tuple[4],
                                            datetime_tuple[6])
        else:
            date_string = "{}:{}:  ".format(datetime_tuple[4],
                                            datetime_tuple[5])
    else:                               # else return normal date string
        date_string = "{}:{}:{}".format(datetime_tuple[4],
                                        datetime_tuple[5],
                                        datetime_tuple[6])
    return date_string
