from time import sleep

from charitybot2.paths import private_api_script_path, console_script_path, overlay_script_path
from charitybot2.start_service import Service, ServiceRunner
from tests.setup_test_database import setup_test_database

test_event_identifier = 'test'
debug = True

if debug:
    setup_test_database(donation_count=10)

api_service = Service(
    name='Private API',
    app=None,
    address='127.0.0.1',
    port=6000,
    debug=debug)

api_runner = ServiceRunner(
    service=api_service,
    file_path=private_api_script_path)

overlay_service = Service(
    name='Overlay',
    app=None,
    address='127.0.0.1',
    port=7000,
    debug=debug)

overlay_runner = ServiceRunner(
    service=overlay_service,
    file_path=overlay_script_path)

console_service = Service(
    name='Test Console',
    app=None,
    address='127.0.0.1',
    port=8000,
    debug=debug)

console_runner = ServiceRunner(
    service=console_service,
    file_path=console_script_path)

try:
    api_runner.run()
    overlay_runner.run()
    console_runner.run()
    while True:
        sleep(1)
except KeyboardInterrupt:
    api_runner.stop_running()
    sleep(1)
    overlay_runner.stop_running()
    sleep(1)
    console_runner.stop_running()
