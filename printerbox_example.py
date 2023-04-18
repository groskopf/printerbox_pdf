import websocket
import rel


def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def on_open(ws):
    print("Opened connection")


if __name__ == "__main__":
    websocket.enableTrace(False)
    # ws = websocket.WebSocketApp("ws://localhost:8000/name_tags/1OPYKBGXVN_1/ws",
    ws = websocket.WebSocketApp("wss://api.printerboks.dk/api/v1/name_tags/1OPYKBGXVN_1/ws",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()
