import asyncio
import json
import logging
import random
import signal
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone


logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("port", nargs="+", type=int)

    def handle(self, *args, **options):
        ports = frozenset(options["port"])
        # Set up event loop.
        loop = asyncio.get_event_loop()
        loop.set_debug(settings.DEBUG)
        # Start the app.
        future = loop.create_task(_run_app(ports))
        future.add_done_callback(_app_done)
        loop.add_signal_handler(signal.SIGTERM, future.cancel)
        loop.add_signal_handler(signal.SIGINT, future.cancel)
        loop.run_forever()


def _app_done(future):
    asyncio.get_event_loop().stop()


async def _run_app(ports):
    loop = asyncio.get_event_loop()
    # Start a server for each port.
    servers = await asyncio.gather(*map(_start_server, ports))
    try:
        await loop.create_future()
    except asyncio.CancelledError:
        # Clean up the servers on shutdown.
        for server in servers:
            server.close()
        await asyncio.gather(*(server.wait_closed() for server in servers))


async def _start_server(port):
    server = await asyncio.start_server(_client_connected, host="127.0.0.1", port=port)
    logger.info("Started server on port %s", port)
    return server


async def _client_connected(reader, writer):
    logger.info("Client connected")
    try:
        while True:
            # Simulate waiting for a bird to be spotted by waiting for a random amount of time.
            await asyncio.sleep(random.randint(1, 3))
            # Generate a simulated bird packet.
            packet = json.dumps({
                "timestamp": timezone.now().isoformat(),
                "species": _create_species_name(),
                "name": _create_name(),
            }).encode()
            # Write the bird packet to the stream.
            writer.write(len(packet).to_bytes(4, "little", signed=False))
            writer.write(packet)
            # Wait for the packet to be sent.
            try:
                await writer.drain()
            except IOError:
                # If the client disconnects, we hear about it as an IOError, so close the connection.
                break
    finally:
        logger.info("Client disconnected")


# Bird species names.

def _create_species_name():
    return " ".join((
        random.choice(_SPECIES_PREFIX),
        random.choice(_SPECIES_SUFFIX),
    ))


_SPECIES_PREFIX = (
    "Blue",
    "Greater",
    "Lesser Spotted",
    "Common",
)

_SPECIES_SUFFIX = (
    "Finch",
    "Tit",
    "Albatross",
    "Gull",
)


# Bird names.

def _create_name():
    return " ".join((
        random.choice(_NAME_TITLE),
        random.choice(_NAME_FIRST),
        random.choice(_NAME_LAST),
    ))


_NAME_TITLE = (
    "Mr",
    "Ms",
    "Lord",
    "Lady",
    "Baron",
    "Baroness",
)

# Taken from https://www.ssa.gov/OACT/babynames/decades/century.html.
_NAME_FIRST = (
    "James",
    "John",
    "Robert",
    "Michael",
    "William",
    "David",
    "Richard",
    "Joseph",
    "Thomas",
    "Charles",
    "Christopher",
    "Daniel",
    "Matthew",
    "Anthony",
    "Donald",
    "Mark",
    "Paul",
    "Steven",
    "Andrew",
    "Kenneth",
    "George",
    "Joshua",
    "Kevin",
    "Brian",
    "Edward",
    "Ronald",
    "Timothy",
    "Jason",
    "Jeffrey",
    "Ryan",
    "Jacob",
    "Gary",
    "Nicholas",
    "Eric",
    "Stephen",
    "Jonathan",
    "Larry",
    "Justin",
    "Scott",
    "Brandon",
    "Frank",
    "Benjamin",
    "Gregory",
    "Raymond",
    "Samuel",
    "Patrick",
    "Alexander",
    "Jack",
    "Dennis",
    "Jerry",
    "Tyler",
    "Aaron",
    "Henry",
    "Jose",
    "Douglas",
    "Peter",
    "Adam",
    "Nathan",
    "Zachary",
    "Walter",
    "Kyle",
    "Harold",
    "Carl",
    "Jeremy",
    "Gerald",
    "Keith",
    "Roger",
    "Arthur",
    "Terry",
    "Lawrence",
    "Sean",
    "Christian",
    "Ethan",
    "Austin",
    "Joe",
    "Albert",
    "Jesse",
    "Willie",
    "Billy",
    "Bryan",
    "Bruce",
    "Noah",
    "Jordan",
    "Dylan",
    "Ralph",
    "Roy",
    "Alan",
    "Wayne",
    "Eugene",
    "Juan",
    "Gabriel",
    "Louis",
    "Russell",
    "Randy",
    "Vincent",
    "Philip",
    "Logan",
    "Bobby",
    "Harry",
    "Johnny",
    "Mary",
    "Patricia",
    "Jennifer",
    "Linda",
    "Elizabeth",
    "Barbara",
    "Susan",
    "Jessica",
    "Sarah",
    "Margaret",
    "Karen",
    "Nancy",
    "Lisa",
    "Betty",
    "Dorothy",
    "Sandra",
    "Ashley",
    "Kimberly",
    "Donna",
    "Emily",
    "Carol",
    "Michelle",
    "Amanda",
    "Melissa",
    "Deborah",
    "Stephanie",
    "Rebecca",
    "Laura",
    "Helen",
    "Sharon",
    "Cynthia",
    "Kathleen",
    "Amy",
    "Shirley",
    "Angela",
    "Anna",
    "Ruth",
    "Brenda",
    "Pamela",
    "Nicole",
    "Katherine",
    "Samantha",
    "Christine",
    "Catherine",
    "Virginia",
    "Debra",
    "Rachel",
    "Janet",
    "Emma",
    "Carolyn",
    "Maria",
    "Heather",
    "Diane",
    "Julie",
    "Joyce",
    "Evelyn",
    "Joan",
    "Victoria",
    "Kelly",
    "Christina",
    "Lauren",
    "Frances",
    "Martha",
    "Judith",
    "Cheryl",
    "Megan",
    "Andrea",
    "Olivia",
    "Ann",
    "Jean",
    "Alice",
    "Jacqueline",
    "Hannah",
    "Doris",
    "Kathryn",
    "Gloria",
    "Teresa",
    "Sara",
    "Janice",
    "Marie",
    "Julia",
    "Grace",
    "Judy",
    "Theresa",
    "Madison",
    "Beverly",
    "Denise",
    "Marilyn",
    "Amber",
    "Danielle",
    "Rose",
    "Brittany",
    "Diana",
    "Abigail",
    "Natalie",
    "Jane",
    "Lori",
    "Alexis",
    "Tiffany",
    "Kayla",
)

# Taken from https://en.geneanet.org/genealogy/1/Surname.php?legacy_script=%2Freferencement%2Fnoms%2Findex.php.
_NAME_LAST = (
    "Smith",
    "Jones",
    "Brown",
    "Johnson",
    "Williams",
    "Miller",
    "Taylor",
    "Wilson",
    "Davis",
    "White",
    "Clark",
    "Hall",
    "Thomas",
    "Thompson",
    "Moore",
    "Hill",
    "Walker",
    "Anderson",
    "Wright",
    "Martin",
    "Wood",
    "Allen",
    "Robinson",
    "Lewis",
    "Scott",
    "Young",
    "Jackson",
    "Adams",
    "Tryniski",
    "Green",
    "Evans",
    "King",
    "Baker",
    "John",
    "Harris",
    "Roberts",
    "Campbell",
    "James",
    "Stewart",
    "Lee",
    "County",
    "Turner",
    "Parker",
    "Cook",
    "Mc",
    "Edwards",
    "Morris",
    "Mitchell",
    "Bell",
    "Ward",
    "Watson",
    "Morgan",
    "Davies",
    "Cooper",
    "Phillips",
    "Rogers",
    "Gray",
    "Hughes",
    "Harrison",
    "Carter",
    "Murphy",
    "Collins",
    "Henry",
    "Foster",
    "Richardson",
    "Russell",
    "Hamilton",
    "Shaw",
    "Bennett",
    "Howard",
    "Reed",
    "Fisher",
    "Marshall",
    "May",
    "Church",
    "Washington",
    "Kelly",
    "Price",
    "Murray",
    "William",
    "Palmer",
    "Stevens",
    "Cox",
    "Robertson",
    "Miss",
    "Clarke",
    "Bailey",
    "George",
    "Nelson",
    "Mason",
    "Butler",
    "Mills",
    "Hunt",
    "Island",
    "Simpson",
    "Graham",
    "Henderson",
    "Ross",
    "Stone",
    "Porter",
    "Wallace",
    "Kennedy",
    "Gibson",
    "West",
    "Brooks",
    "Ellis",
    "Barnes",
    "Johnston",
    "Sullivan",
    "Wells",
    "Hart",
    "Ford",
    "Reynolds",
    "Alexander",
    "Co",
    "Cole",
    "Fox",
    "Holmes",
    "Day",
    "Chapman",
    "Powell",
    "Webster",
    "Long",
    "Richards",
    "Grant",
    "Hunter",
    "Webb",
    "Thomson",
    "Wm",
    "Lincoln",
    "Gordon",
    "Wheeler",
    "Street",
    "Perry",
    "Black",
    "Lane",
    "Gardner",
    "City",
    "Lawrence",
    "Andrews",
    "Warren",
    "Spencer",
    "Rice",
    "Jenkins",
    "Knight",
    "Armstrong",
    "Burns",
    "Barker",
    "Dunn",
    "Reid",
)
