import asyncio
import json
import logging

import websockets
from buzzer.models import *


logger = logging.getLogger('ws.server')

students_queue = []
inst_queue = []
clients = []
first_connection = True

@asyncio.coroutine
def handle_client_messages(websocket, qq):
    while True:
        json_msg = yield from websocket.recv()
        logger.info("Socket %x <=! %s", id(websocket), json_msg)
        print(json_msg)
        if json_msg is None:
            # Socket has closed
            return
        print(json_msg)
        rcvd_msg = json.loads(json_msg)
        msg = json.loads(rcvd_msg['_data']['message'])


        if msg['client_type'] == "instructor":
            print("Instructor added")
            inst_queue.append(qq)
        elif msg['client_type'] == "student":
            quizID = int(msg['quizID'])
            rcvd_msg['_data']['message'] = generate_result_msg(quizID)

            print(rcvd_msg)
            json_msg = json.dumps(rcvd_msg)
            print(json_msg)
            print(type(json_msg))
            # Send the message to all clients
            for q in inst_queue:
                yield from q.put(json_msg)


@asyncio.coroutine
def push_messages(websocket, q):
    while True:
        msg = yield from q.get()

        if not websocket.open:
            return

        logger.info("WS %x: pushing message %s", id(websocket), msg)
        yield from websocket.send(msg)


@asyncio.coroutine
def client_handler(websocket, uri):
    logger.info("New client, websocket %x", id(websocket))
    q = asyncio.Queue()
    clients.append(q)

    #yield from websocket.send(json.dumps({
    #    "_event": "showMessage",
    #    "_data": {
    #        "message": "Welcome to the chat!"
    #    },
    #}))

    tasks = [
        handle_client_messages(websocket, q),
        push_messages(websocket, q),
    ]

    yield from asyncio_wait(tasks)
    logger.info("client_handler() done")


def run_server(host, port):
    logger.info("Starting control server on %s:%d", host, port)
    print("Starting control server on %s:%d\n", host, port);
    start_server = websockets.serve(client_handler, host, port)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


def asyncio_wait(coros):
    """ Helper that augments asyncio.wait with better exception handling
    """
    done, pending = yield from asyncio.wait(
        [asyncio.Task(coro) for coro in coros],
        return_when=asyncio.FIRST_EXCEPTION,
    )

    failed = list(filter(lambda task: task.exception(), done))
    if failed:
        raise failed[0].exception()

def generate_result_msg(quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    question_list = Question.objects.filter(quiz=quiz)
    choice_list = []
    result = {}
    for questions in question_list:
        choices_list = Choice.objects.filter(question=questions)
        votes_per_choice = {}
        for choice in choices_list:
            choice_list.append(choice)
            votes_per_choice[choice.id] = choice.votes
        result[questions.id] = votes_per_choice

    return result
