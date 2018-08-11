
# Dictionaries per language with all the messages of GS1 cloud
# Extra languages shoud be added to the dictonary 'languages' at the end of this file

en = {
    "E001": "Integrity failed: The length of this GTIN is invalid.",
    "E002": "Integrity failed: Incorrect check digit.",
    "E003": "Integrity failed: String contains alphanumerical characters.",
    "E004": "Incorrect number.That GS1 prefix(3 - digit country code) does not exist.",
    "E005": "Incorrect number based on GS1 Prefix reserved for special use.",
    "S001": "Unknown number, no information can be returned.",
    "S002": "Unknown GTIN from a license issued to: ",
    "S003": "Active GTIN from a license issued to: ",
    "S004": "Inactive GTIN from a license issued to: ",
    "S005": "Active GTIN from a license issued to: "}

nl = {
    "E001": "Onjuiste structuur: De lengte van de GTIN is niet correct.",
    "E002": "Onjuiste structuur: Niet correct controle getal.",
    "E003": "Onjuiste structuur: De GTIN bevat alfanumerieke karakters.",
    "E004": "Onjuist nummer. De GS1 prefix(3-cijferige landcode) bestaat niet.",
    "E005": "Onjuist nummer: de GS1 Prefix is gereserveerd voor speciale toepassingen.",
    "S001": "Onbekend nummer, er kan geen informatie gegeven worden.",
    "S002": "Onbekende GTIN van een licentie verleend aan: ",
    "S003": "Actieve GTIN van een licentie verleend aan: ",
    "S004": "Inactieve GTIN van een licentie verleend aan: ",
    "S005": "Actieve GTIN van een licentie verleend aan: "}


# Dictionary with the available languages
languages = {"nl": nl, "en": en}
