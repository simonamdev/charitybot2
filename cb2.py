from charitybot2.charitybot2 import create_parser, CharityBot

args = create_parser().parse_args()
CharityBot(args=args)
