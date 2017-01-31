from charitybot2.reporter.external_api.external_api import create_api_process_parser, start_api

args = create_api_process_parser().parse_args()
start_api(args=args)
