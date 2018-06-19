# CRFS RFeye Birdwatcher

Connects to a network of RFeye Birdwatcher nodes, and streams live
bird events into a database.


# Architecture

A number of pieces of hardware, known as "nodes", are deployed in national
parks around the country. These nodes contain sophisticated detection
apparatus allowing them to spot birds and classify them by species.
It can even tell the bird's given name!

The Birdwatcher application consists of the following processes:


## Birdwatcher daemon

The Birdwatcher daemon connects to the node network and receives live bird
events in real-time. It logs all spotted birds to the database.


## Web UI

The web UI allows admin users to view the list of birds that have been
logged to the database.

The web UI also allows nodes to be added, edited, and removed. As nodes
are added, edited and removed, the Birdwatcher daemon will respond to
changes and connect/disconnect from nodes as appropriate.


# Birdwatcher protocol

Each Birdwatcher node listens for incoming TCP connections on a port
(specified in the ``Node`` database model).

For each connected client, it will send live bird event packets. A bird
event packet consists of:

- **Packet length:** A 32 bit unsigned, little-endian integer in binary
  encoding.
- **Packet content:** A UTF-8 JSON object.

The event JSON packet looks like this:

``` js
{
  "timestamp": string,  // ISO-8601 timestamp.
  "species": string,  // The species name.
  "name": string,  // The bird's given name.
}
```

When the Birdwatcher daemon receives and parses a bird event packet, it
will:

1. Create a ``Species`` model corresponding to the species name. If such
   a species already exists in the database, it will load it from the
   database instead.
2. Create a ``Bird`` model. The bird will be tagged with the species,
   origin node, timestamp and given name.


# Birdwatcher node simulator

A Django management command called ``runnodes`` can be used to simulate
a Birdwatcher node.

For example, to run two simulated nodes on ports 9999 and 9998:

``` bash
./manage.py runnodes 9999 9998
```

The simulated nodes listen on `127.0.0.1`, using the ports specified.


# The task!

Your task is to write the Birdwatcher daemon. This will be implemented
as a Django management command called ``connectnodes``. The command takes
no arguments, and will perform the following:

- Regularly check the current list of nodes in the database.
- For each node in the database, maintain a connection to the node.
- If a node has it's IP address or port changed, reconnect to the node.
- If a node is deleted, disconnect from the node.
- For each active connection, parse incoming bird event packets and log
  them to the database.

Things to consider:

- The database models have already been defined, and are correct.
- The daemon should be implemented using the ``asyncio`` event loop.
- Blocking the event loop with database or network IO is bad!
- The daemon must handle downtime and network errors, and attempt to
  maintain a connection to each node despite this.
- The daemon can assume that the nodes send data using the correct
  protocol.
- Using the Python logging framework will greatly assist our understanding
  of your solution!


# Testing your solution

The following test will be run on your solution:

1. A blank database with a single superuser account will be created. The
   web UI will be started using the ``runserver`` management command.

2. Two simulated nodes will be started on ports 9999 and 9998 using the
   ``runnodes`` management command.

3. The Birdwatcher deamon will be started using the ``connectnodes``
   management command.

4. Using the web UI, three nodes will be created, listening on ports
   9999, 9998 and 9997.

   **Expected behavior:** The Birdwatcher daemon soon starts logging bird
   events to the database.

5. The Birdwatcher daemon will run for 1 minute.

6. The ``runnodes`` simulator will be stopped.

   **Expected behavior:** The Birdwatcher deamon gracefully handles the
   disconnect.

7. The ``runnodes`` simulator will be started.

   **Expected behavior:** The Birdwatcher deamon soon reconnects to the
   nodes and starts logging bird events to the database.

8. The node listening on port 9999 will be deleted using the web UI.

   **Expected behavior:** The Birdwatcher daemon soon disconnects from the
   node listening on port 9999.

9. The node listening on port 9998 will have it's port changed to 9999
   using the web UI.

   **Expected behavior:** The Birdwatcher daemon soon disconnects from the
   node on port 9998, then reconnects on port 9999.


# Any questions?

Please email dhall@crfs.com if you have any questions regarding this
problem.
