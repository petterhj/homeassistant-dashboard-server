import json
from random import randint

from websockets import connect, ConnectionClosed


async def socket_service_call(
    ha_api_url,
    ha_token,
    domain,
    service,
    target={},
    service_data={},
):
    uri = "ws://{}websocket".format(ha_api_url.split("://")[1])
    call_id = randint(100, 200)

    async with connect(uri) as websocket:
        try:
            async for data in websocket:
                data = json.loads(data)

                if data["type"] == "auth_required":
                    await websocket.send(
                        json.dumps(
                            {
                                "type": "auth",
                                "access_token": ha_token,
                            }
                        )
                    )
                elif data["type"] == "auth_invalid":
                    raise Exception(data["message"])
                elif data["type"] == "auth_ok":
                    await websocket.send(
                        json.dumps(
                            {
                                "id": call_id,
                                "type": "call_service",
                                "domain": domain,
                                "service": service,
                                "service_data": service_data,
                                "target": target,
                                "return_response": True,
                            }
                        )
                    )
                elif data["type"] == "result" and data["id"] == call_id:
                    if not data["success"]:
                        raise Exception(
                            f"{data['error']['code']}: {data['error']['message']}"
                        )
                    return data["result"]["response"]

        except ConnectionClosed as e:
            raise Exception(f"Websocket connection closed: {e}")
