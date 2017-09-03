import time
from charitybot2.models.donation import Donation
from tiltify2.tiltify import Tiltify2, Order
from dateutil import parser


class TiltifySource:
    def __init__(self, event_identifier, api_key, limit=25):
        self._event_identifier = event_identifier
        self._tiltify = Tiltify2(api_key=api_key)
        self._limit = limit

    def get_new_donations(self, known_donation_ids=()):
        donations = self.get_donations()
        donations = [donation for donation in donations if donation['id'] not in known_donation_ids]
        return [self.__convert_to_donation(donation) for donation in donations]

    def get_donations(self):
        return self._tiltify.get_donations(order_by=Order.CREATED_AT, donation_order=Order.DESC, limit=self._limit)

    def get_all_donations(self):
        return self._tiltify.get_donations(order_by=Order.CREATED_AT, donation_order=Order.DESC)

    def __convert_to_donation(self, donation):
        # 2014-09-17 16:06:21 -0400
        return Donation(
            amount=donation['amount'],
            event_identifier=self._event_identifier,
            timestamp=time.mktime(parser.parse(donation['created']).timetuple()),
            external_reference=str(donation['id']),
            donor_name=donation['name'],
            notes=donation['comment']
        )
