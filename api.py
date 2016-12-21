from charitybot2.reporter.external_api.external_api import start_api, create_api_process_parser

args = create_api_process_parser().parse_args()
start_api(args=args)
