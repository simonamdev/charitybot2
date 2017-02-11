# CharityBot2

## Aim

CharityBot originally started as a means to enable twitch streamers to focus on entertaining their audience during charity streams.
A common scene during charity streams was a streamer who would ask if a donation had been received, pause the game and
navigate to the donation website to confirm. This would very often break up the pacing of the broadcast which could
alienate viewers.

Instead of doing this manually, CB2 takes care of checking the donation amount on the fundraising website and
updating the amount raised automatically on the stream overlay, helping the
charity streamer focus on what they do best: entertaining viewers in aid of a good cause.

CB2 also offers real time feedback 

## CharityBot2 beta tests

CharityBot was field tested during Gameblast16, a weekend of streaming used to raise funds for the amazing charity [Special Effect](http://www.specialeffect.org.uk/) who work with disabled people to enable them to enjoy gaming. The current develop build of CB2 is being publicly field tested during [Gameblast17](https://www.gameblast17.com/)

## How to use CB2 as a streamer

- Read the instructions [here](https://www.gameblast17.com/wp-content/uploads/2017/02/CB2-GB17-Setup-Guide-v2-2.pdf)

## Under refurbishment

I am currently reworking the architecture of CB2 to improve testability and to deal with some accrued technical debt, so pull requests (unless they're more tests or bug fixes) are currently not recommended, however still appreciated! The aim of the refactor is to enable CB2 to handle several hundred simultaneous fundraisers without breaking a sweat.

## CharityBot2 Requirements

- Python 3.x+
- SQLite

## Testing Requirements

- Chromedriver (for E2E tests)
- JustGiving API key
- Twitch account API key

## Licence

GPLv3 Licence
