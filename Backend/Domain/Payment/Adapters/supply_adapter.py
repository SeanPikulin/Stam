from Backend.response import Response
from werkzeug.security import generate_password_hash
from Backend.Domain.Payment.OutsideSystems.outside_supplyment import OutsideSupplyment


class SupplyAdapter:

    def __init__(self):
        self.__outside_supplyment = OutsideSupplyment()
        self.__hashes = dict()

    def deliver(self, product_ids_to_quantity, address):
        # Temporal implementation, will be change with the real implementation of OutsideSupplyment.
        # Assuming outside supplyment returns boolean, wrapping with response to include message later.
        hashed_address = generate_password_hash(address, method="sha256")
        if address not in self.__hashes:
            self.__hashes[address] = hashed_address
        answer = self.__outside_supplyment.deliver(product_ids_to_quantity, self.__hashes[address])
        if isinstance(answer, Response):        # I wanted for test purposes to return Response, and I can't trust real outside system to return Response
            return answer
        return Response(success=answer)
