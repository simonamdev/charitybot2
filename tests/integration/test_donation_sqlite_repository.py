from charitybot2.persistence.donation_sqlite_repository import DonationSQLiteRepository


class TestDonationSQLiteRepository:
    test_donation_repository = None

    def setup_method(self):
        self.test_donation_repository = DonationSQLiteRepository(debug=True)

    def teardown_method(self):
        self.test_donation_repository.close_connection()




class TestDonationSQLiteRepositoryExceptions:
    test_donation_repository = None

    def setup_method(self):
        self.test_donation_repository = DonationSQLiteRepository(debug=True)

    def teardown_method(self):
        self.test_donation_repository.close_connection()
