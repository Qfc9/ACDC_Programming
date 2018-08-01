#!/usr/bin/env python3
import standards
import cgi
from mysql_utils import get_connection


def main():
    """
    Main function for battle details page
    """

    # Getting information for variables in the url
    fields = cgi.FieldStorage()
    c1 = fields.getvalue("c1", None)
    c2 = fields.getvalue("c2", None)

    # If they aren't set, error out
    if c1 is None or c2 is None:
        standards.displayError()
        return

    body = standards.getBody("templates/battle-detail.html")

    # Using the first and second combatant, get the fight information
    query = "SELECT winner_id, DATE_FORMAT(start, '%c-%d-%Y'), "\
            "(DATE_FORMAT(start, '%S') + DATE_FORMAT(finish, '%S')) "\
            "FROM Fight "\
            "WHERE combatant_one = {} AND combatant_two = {};".format(c1, c2)
    result = standards.getSQLData(query)

    # Error out if there isn't a result
    if len(result) < 1:
        standards.displayError()
        return

    # Unpacking the result, there should only be 1 result
    winner, date, length = result[0]

    # Getting combatant information
    query = "SELECT c1.name, c2.name, winner.name "\
            "FROM Combatant AS c1, Combatant AS c2, Combatant AS winner "\
            "WHERE c1.id = {} AND c2.id = {} AND winner.id = {};".format(c1, c2, winner)
    result = standards.getSQLData(query)

    # Erroring out if there is no combatant information
    if len(result) < 1:
        standards.displayError()
        return

    # Unpacking results, should only be 1 result
    c1Name, c2Name, winner = result[0]

    # Formating based on pluralization
    row = "<tr><td>{}</td><td>{} {}</td></tr>"
    if length > 1:
        row = row.format(date, length, "seconds")
    else:
        row = row.format(date, length, "second")

    standards.displayPage(body.format(c1Name, c2Name, winner, row))

if __name__ == "__main__":
    main()
