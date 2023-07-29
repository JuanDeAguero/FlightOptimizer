
# ~ MAIN ~
# This module is the starting point of the application.
# Handles user interaction with the GUI and the Flight Network.
# ______________________________
# Copyright (c) Juan Martin 2021

from flight_network import FlightNetwork
import gui

def on_app_start() -> None:
    """ Called once when the app starts. """

    print( "[INFO] App started successfully." )
    gui.hide_all_codes()
    gui.set_departure_text( "SAN" )
    gui.set_arrival_text( "JFK" )
    on_search_clicked()

def on_search_clicked() -> None:
    """ Called when the search button is pressed. """

    departure = gui.get_departure()
    arrival = gui.get_arrival()

    # Check user inputs are valid
    if departure not in network._flights.keys() or arrival not in network._flights.keys():
        print( "[ERROR] Invalid airport code." )
        return
    if departure == arrival:
        print( "[ERROR] No need to take a plane!" )
        return

    gui.hide_all_path_widget()
    gui.hide_border()

    # Get paths from the network
    paths = network.get_paths( departure, arrival )

    # Creeate lists of texts, distances and prices for the GUI items.
    # (using the paths extracted from the network)
    texts = []
    distances = []
    prices = []
    for path in paths:
        text = path[0]
        distance = 0
        cost = 0
        for i in range( len( path ) - 1 ):
            text += " > " + path[i+1]
            flight = network.get_connecting_flight( path[i], path[i+1] )
            distance += flight.get_distance()
            cost += int( flight.get_cost() )
        texts.append( text )
        distances.append( distance )
        prices.append( cost )

    # Sort distances and update texts and prices accordingly.
    global sorted_texts
    sorted_distances = sorted( distances )
    sorted_texts = []
    sorted_prices = []
    used_indices = []
    for sorted_distance in sorted_distances:
        for i in range( len( distances ) ):
            if distances[i] == sorted_distance:
                if i not in used_indices:
                    used_indices.append( i )
                    sorted_texts.append( texts[i] )
                    sorted_prices.append( prices[i] )
    sorted_distances = sorted_distances[:7]
    sorted_texts = sorted_texts[:7]
    sorted_prices = sorted_prices[:7]

    # Use texts, distances and prices to update the GUI items.
    for i in range( 7 ):
        if i < len( sorted_texts ):
            gui.set_flight_path_text( sorted_texts[i], i )
            gui.set_flight_path_distance( "Distance: " + str( sorted_distances[i] ) + " miles", i )
            gui.set_flight_path_price( "Price: $" + str( sorted_prices[i] ), i )
        else:
            gui.set_flight_path_text( "", i )
            gui.set_flight_path_distance( "", i )
            gui.set_flight_path_price( "", i )

    n = len( sorted_distances )
    if n > 0:
        gui.show_border()
    for i in range( n ):
        gui.show_path_widget( i )

    on_flight_path_clicked( 0 )

    print( "[INFO] " + str( len( texts ) ) + " flight combinations found." )

def on_flight_path_clicked( index: int ) -> None:
    """ Called when one of the flight path items is clicked.
        index: item index. """

    if index + 1 > len( sorted_texts ):
        return

    gui.set_border_location( 988, 188 + ( 100 * index ) )
    gui.hide_all_codes()
    gui.uncheck_show_airport_codes()

    # Check that the airport codes are included in the GUI map.
    code1 = sorted_texts[index][0] + sorted_texts[index][1] + sorted_texts[index][2]
    code2 = sorted_texts[index][6] + sorted_texts[index][7] + sorted_texts[index][8]
    if not gui.check_code_in_map( code1 ) or not gui.check_code_in_map( code2 ):
        print( "[WARNING] Airport code not in the map." )
        return
    if len( sorted_texts[index] ) > 9:
        code3 = sorted_texts[index][12] + sorted_texts[index][13] + sorted_texts[index][14]
        if not gui.check_code_in_map( code3 ):
            print( "[WARNING] Airport code not in the map." )
            return
        gui.show_code( code3 )
    gui.show_code( code1 )
    gui.show_code( code2 )

    print( "[INFO] Item #" + str( index + 1 ) + " selected." )

def on_show_airport_codes_checked() -> None:
    """ Called when the "Show all airport codes" checkbox is clicked
        and its state is checked. """
    gui.show_all_codes()
    print( "[INFO] Airport codes visible." )

def on_show_airport_codes_unchecked() -> None:
    """ Called when the "Show all airport codes" checkbox is clicked
        and its state is unchecked. """
    gui.hide_all_codes()
    print( "[INFO] Airport codes hidden." )

if __name__ == "__main__":

    # 1. Create and load the Flight Network
    global network
    network = FlightNetwork()
    network.load( "flights.csv" )
    
    # 2. Bind all the GUI callbacks
    gui.set_on_app_start( on_app_start )
    gui.set_on_search_clicked( on_search_clicked )
    gui.set_on_flight_path_1_clicked( lambda: on_flight_path_clicked( 0 ) )
    gui.set_on_flight_path_2_clicked( lambda: on_flight_path_clicked( 1 ) )
    gui.set_on_flight_path_3_clicked( lambda: on_flight_path_clicked( 2 ) )
    gui.set_on_flight_path_4_clicked( lambda: on_flight_path_clicked( 3 ) )
    gui.set_on_flight_path_5_clicked( lambda: on_flight_path_clicked( 4 ) )
    gui.set_on_flight_path_6_clicked( lambda: on_flight_path_clicked( 5 ) )
    gui.set_on_flight_path_7_clicked( lambda: on_flight_path_clicked( 6 ) )
    gui.set_on_show_airport_codes_checked( on_show_airport_codes_checked )
    gui.set_on_show_airport_codes_unchecked( on_show_airport_codes_unchecked )

    # 3. Run the app
    gui.run_app()
