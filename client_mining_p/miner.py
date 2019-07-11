import hashlib
import requests  # pylint: disable=F0401

import sys


# TODO: Implement functionality to search for a proof
def proof_of_work(last_proof):
    # just pulled from what we did in the other file
    print("looking...")
    proof = 0
    while valid_proof(last_proof, proof) is False:
        proof += 1
    print("found a proof!")
    return proof


def valid_proof(last_proof, proof):
    # again, just pulled from the walkthrough
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:6] == "000000"


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    # Run forever until interrupted
    while True:
        # TODO: Get the last proof from the server and look for a new one
        last_proof = requests.get(url=f'{node}/last_proof')
        #print(f"last proof: {last_proof}")
        proof = proof_of_work(last_proof.json().get('proof'))
        # TODO: When found, POST it to the server {"proof": new_proof}
        answer = requests.post(url=f'{node}/mine', json={"proof": proof})
        # TODO: If the server responds with 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        if answer.json().get('message') == "New Block Forged":
            print("Successfully mined a new coin")
            coins_mined += 1
            print(f"you now have {coins_mined} coins")
        else:
            print("invalid coin")
