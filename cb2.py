from charitybot2.charitybot2 import create_parser, CharityBot

args = create_parser().parse_args()
bot = CharityBot(args=args)
bot.initialise_bot()
bot.start_bot()
