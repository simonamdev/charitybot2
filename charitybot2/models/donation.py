import json
import time
import uuid
from json import JSONDecodeError


class InvalidDonationException(Exception):
    pass


class Donation:
    __rounding_amount = 2
    keys_required = (
        'amount',
        'event_identifier',
        'timestamp',
        'internal_reference',
        'external_reference',
        'donor_name',
        'notes',
        'valid'
    )

    def __init__(self,
                 amount,
                 event_identifier,
                 currency_code,
                 timestamp=None,
                 internal_reference=None,
                 external_reference=None,
                 donor_name=None,
                 notes=None,
                 valid=True):
        self._amount = amount
        self._event_identifier = event_identifier
        self._currency_code = currency_code
        if timestamp is None:
            timestamp = int(time.time())
        self._timestamp = timestamp
        self._internal_reference = internal_reference
        self._external_reference = external_reference
        self._donor_name = donor_name
        self._notes = notes
        self._valid = valid
        self.__validate_donation()
        self.__parse_donation_amount()

    def __str__(self):
        return 'Donation of {} made by {} at {} in event: {} with notes: {} and validity: {}'.format(
            self._amount,
            self._donor_name,
            self._timestamp,
            self._event_identifier,
            self._notes,
            self._valid
        )

    def __validate_donation(self):
        if self._amount == '' or self._amount is None:
            raise InvalidDonationException('Donation amount cannot be an empty string')
        if not isinstance(self._event_identifier, str) or self._event_identifier == '':
            raise InvalidDonationException('Invalid Event identifier passed')
        if self._amount == 0:
            raise InvalidDonationException('Donation cannot have a value of 0')
        if self._timestamp < 0:
            raise InvalidDonationException('Invalid timestamp passed')
        self.__generate_internal_reference()
        if not isinstance(self._internal_reference, str) or len(self._internal_reference) == 0:
            raise InvalidDonationException('Invalid internal reference passed')

    def __generate_internal_reference(self):
        if self._internal_reference is None:
            self._internal_reference = str(uuid.uuid4())

    def __parse_donation_amount(self):
        if isinstance(self._amount, str):
            self._amount = self._amount.replace(',', '')
            try:
                self._amount = float(self._amount)
            except ValueError:
                raise InvalidDonationException('Cannot parse input string properly')
        self._amount = round(self._amount, self.__rounding_amount)

    @property
    def amount(self):
        return self._amount

    @property
    def event_identifier(self):
        return self._event_identifier

    @property
    def currency_code(self):
        return self._currency_code

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def internal_reference(self):
        return self._internal_reference

    @property
    def external_reference(self):
        return self._external_reference

    @property
    def donor_name(self):
        return self._donor_name

    @property
    def notes(self):
        return self._notes

    @property
    def validity(self):
        return self._valid

    def to_dict(self):
        return dict(
            amount=self.amount,
            event_identifier=self.event_identifier,
            currency_code=self.currency_code,
            timestamp=self.timestamp,
            internal_reference=self.internal_reference,
            external_reference=self.external_reference,
            donor_name=self.donor_name,
            notes=self.notes,
            valid=self.validity)

    def to_json(self):
        return json.dumps(self.to_dict())

    @staticmethod
    def from_dict(donation_dict):
        if not isinstance(donation_dict, dict):
            raise InvalidDonationException('To create a donation from a dictionary, a dict is required')
        try:
            donation = Donation(
                amount=float(donation_dict.get('amount')),
                event_identifier=donation_dict.get('event_identifier'),
                currency_code=donation_dict.get('currency_code'),
                timestamp=int(donation_dict.get('timestamp')),
                internal_reference=donation_dict.get('internal_reference'),
                external_reference=donation_dict.get('external_reference'),
                donor_name=donation_dict.get('donor_name'),
                notes=donation_dict.get('notes'),
                valid=bool(donation_dict.get('valid'))
            )
        except Exception:
            raise InvalidDonationException('Unable to create donation from given Dict data')
        return donation

    @staticmethod
    def from_json(donation_json):
        donation = None
        try:
            donation = Donation.from_dict(json.loads(donation_json))
        except JSONDecodeError:
            raise InvalidDonationException('Unable to create donation from given JSON data: {}'.format(donation_json))
        return donation
