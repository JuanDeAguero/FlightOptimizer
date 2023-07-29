# Copyright (c) Juan Martin 2021

import csv

class Flight:
    """ An edge in the FlightNetwork graph which represents a single Flight.
        departure: code of the departure airport
        arrival:   code of the arrival airport
        distance:  travel distance in miles
        cost:      travel cost in US dollars
        airline:   code of the airline company """

    _departure: str
    _arrival: str
    _distance: int
    _cost: float
    _airline: str

    def __init__( self, departure: str, arrival: str, distance: int, cost: float, airline: str ) -> None:
        self._departure = departure
        self._arrival = arrival
        self._distance = distance
        self._cost = cost
        self._airline = airline

    def get_distance( self ) -> int:
        return self._distance

    def get_cost( self ) -> float:
        return self._cost

class FlightNetwork:
    """ Abstract representation of a flight network implemented as a graph.
        Flight represents the edges and the vertices are the airports (str).
        flights: dictionary storing airport as keys an the set of outgoing flight as values.
                 { Airport: { Flight, Flight, ... }, Airport: { Flight, Flight, ... }, ... } """

    _flights: dict()

    def load( self, file_path: str ) -> None:
        """ Load the data from the given csv file into the _flights dictionary. """

        self._flights = dict()

        c = 0
        connections = []

        with open( file_path ) as csv_file:
            reader = csv.reader(csv_file)

            for row in reader:

                # This value can be modified to reduce the loading time at the start.
                limit = 1100000

                percentage = ( c / limit ) * 100
                log = str( "Loading graph... [" + str( int( percentage ) ) + "%] [" + str( c ) + "/" + str( 1100000 ) + "]" )
                print( log, end="\r" )

                if c == 0:
                    c += 1
                    continue
                elif c > limit:
                    break
                c += 1

                # Check that there are not two flight with the same departure and destination
                connection = ( row[0], row[1] )
                if connection not in connections:
                    connections.append(connection)

                    departure = row[0]
                    arrival = row[1]

                    # Create the Flight class using the values in row
                    flight = Flight( departure, arrival, int(row[2]), float(row[3]), row[4] )

                    if departure not in self._flights:
                        self._flights[departure] = set()
                    if arrival not in self._flights:
                        self._flights[arrival] = set()
                    self._flights[departure].add( flight )

        p = " "
        for _ in range( 50 ):
            p += " "

        print( "[INFO] Graph fully loaded." + p )

    def get_paths( self, departure: str, arrival: str ) -> list():
        """ Returns all the possible paths between two airports in the network. """

        paths = []
        self._get_paths_recursion( departure, arrival, paths=paths )
        return paths

    def _get_paths_recursion( self, departure: str, arrival: str,
                              visited = set(), path = list(), paths = list() ) -> None:
        """ Recursive helper of get_paths """

        visited.add( departure )
        path.append( departure )
        if len( path ) < 4:
            # Base case
            if departure == arrival:
                paths.append( path.copy() )
            else:
                for flight in self._flights[departure]:
                    airport = flight._arrival
                    if airport not in visited:
                        # Recursive step
                        self._get_paths_recursion( airport, arrival, visited, path, paths )
        path.pop()
        visited.remove( departure )

    def get_connecting_flight( self, departure: str, arrival: str ) -> Flight:
        """ Returns the flight class between two connected airports. """

        flights = self._flights[departure]
        for flight in flights:
            if flight._arrival == arrival:
                return flight
        print( "[ERROR] " + departure + " and " + arrival + " are NOT connected!" )
        return Flight( "", "", 0, 0, "" )
