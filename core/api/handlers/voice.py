"""Handles voice requirements
"""
from typing import Dict

from fastapi import HTTPException, status

from core.api.common.typing import JSONStructure
from core.api.common.utils import ws_send
from core.api.config import get_settings
from core.api.models.voice import Speak

settings = get_settings()


def speaking(speak: Speak) -> JSONStructure:
    """Send a speak request to Core

    Send `speak` message to the bus with the utterance to speak.

    :param speak: Which utterance ans lang to send
    :type speak: Speak
    :return: Return JSON dict with the utterance and the lang
    :rtype: JSONStructure
    """
    try:
        payload: Dict = {
            "type": "speak",
            "data": {"utterance": speak.utterance, "lang": speak.lang},
        }
        ws_send(payload)
        return payload["data"]
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="unable to send the utterance",
        ) from err


def stop() -> JSONStructure:
    """Send a stop speech request to Core

    Send `core.stop` message to the bus to stop the speech.

    :return: Return HTTP 204 or 400
    :rtype: int
    """
    try:
        payload: Dict = {"type": "core.stop"}
        ws_send(payload)
        return status.HTTP_204_NO_CONTENT
    except Exception as err:
        print(err)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="unable to stop the speech"
        ) from err


def mute() -> JSONStructure:
    """Send a microphone mute request to Core

    Send `core.mic.mute` message to the bus to mute the microphone.

    :return: Return HTTP 204 or 400
    :rtype: int
    """
    try:
        payload: Dict = {"type": "core.mic.mute"}
        ws_send(payload)
        return status.HTTP_204_NO_CONTENT
    except Exception as err:
        print(err)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="unable to mute microphone"
        ) from err


def unmute() -> JSONStructure:
    """Send a microphone unmute request to Core

    Send `core.mic.unmute` message to the bus to unmute the microphone.

    :return: Return HTTP 204 or 400
    :rtype: int
    """
    try:
        payload: Dict = {"type": "core.mic.unmute"}
        ws_send(payload)
        return status.HTTP_204_NO_CONTENT
    except Exception as err:
        print(err)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="unable to unmute microphone",
        ) from err


def listen() -> JSONStructure:
    """Send a recording request to CORE

    Send `core.mic.listen` message to the bus to start the recording.

    :return: Return HTTP 204 or 400
    :rtype: int
    """
    try:
        payload: Dict = {"type": "core.mic.listen"}
        ws_send(payload)
        return status.HTTP_204_NO_CONTENT
    except Exception as err:
        print(err)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="unable to start the recording",
        ) from err


def handle_utterance(message) -> JSONStructure:
    """Send a recording request to CORE

    Send `recognizer_loop:utterance` message to the bus to get response.

    :return: Return HTTP 204 or 400
    :rtype: int
    """
    try:
        payload: Dict = {
            "type": "recognizer_loop:utterance",
            "data": {
                "utterances": [message.prompt],
                "context": {
                    "client_name": "core_cli",
                    "source": "debug_cli",
                    "destination": ["skills"],
                },
            },
        }
        # TODO: get response from intent_service
        response = ws_send(payload, wait_for_message="core.utterance.response")
        # print(f"response: {response.get('data', {}).get('response', {})}")
        content = response.get("data", {}).get("response", {})
        return {"done": True, "message": {"content": content}}
    except Exception as err:
        print(err)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="unable to send message to bus",
        ) from err
