import asyncio
import logging
from anseo import keyinterface


async def process_keystrokes(ki, key_q):
    while True:
        keypress = await key_q.get()
        if keypress:
            print('Key Press: %s' % (keypress, ))


async def main():
    logging.basicConfig(level=logging.DEBUG)
    key_q = asyncio.Queue()

    # ki = keyinterface.KeyInterface(keyinterface.Implementation.KEYBOW)
    ki = keyinterface.KeyInterface(keyinterface.Implementation.SIMULATED)

    script = [
        'down 1',
        'sleep 0.2',
        'up 1',
        'down 0',
        'sleep 0.6',
        'up 0'
    ]

    ki.setup(script=script)

    seq_l = keyinterface.KeySequenceListener(ki, listen_for=[keyinterface.KeySequence.SINGLE, keyinterface.KeySequence.HOLD])

    await asyncio.gather(seq_l.produce(key_q), process_keystrokes(ki, key_q))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
