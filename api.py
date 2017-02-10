from charitybot2.private_api.private_api import create_api_process_parser, start_api

args = create_api_process_parser().parse_args()
start_api(args=args)
