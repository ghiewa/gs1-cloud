
# Dictionaries per language with all the return messages of GS1 cloud
# Extra languages should be added to the dictonary 'languages' at the end of this file

de = {
    "E001": "Integritaetsfehler: Die Laenge dieser GTIN ist ungueltig.",
    "E002": "Integritaetsfehler: Die Pruefziffer ist nicht korrekt",
    "E003": "Integritaetsfehler: Die Zeichenkette enthaelt alphanumerische Zeichen",
    "E004": "Falsche Nummer. Dieser GS1-Praefix (3-stelliger Laendercode) existiert nicht",
    "E005": "Falsche Nummer. Dieser GS1-Praefix ist reserviert für spezielle Anwendungen",
    "E006": "Falsche Nummer. Dieser GS1-Praefix wurde nicht vergeben",
    "S001": "Unbekannte Nummer. Es kann keine Information gezeigt werden",
    "S002": "Unbekannte GTIN einer Lizenz vergeben an: ",
    "S003": "Aktive GTIN einer Lizenz vergeben an: ",
    "S004": "Inaktive GTIN einer Lizenz vergeben an: ",
    "S005": "Aktive GTIN einer Lizenz vergeben an: "
}

en = {
    "E001": "Integrity failed: The length of this GTIN is invalid.",
    "E002": "Integrity failed: Incorrect check digit.",
    "E003": "Integrity failed: String contains alphanumerical characters.",
    "E004": "Incorrect number. That GS1 prefix(3 - digit country code) does not exist.",
    "E005": "Incorrect number based on GS1 Prefix reserved for special use.",
    "E006": "Incorrect number. That GS1 company prefix has not been assigned.",
    "S001": "Unknown number, no information can be returned.",
    "S002": "Unknown GTIN from a license issued to: ",
    "S003": "Active GTIN from a license issued to: ",
    "S004": "Inactive GTIN from a license issued to: ",
    "S005": "Active GTIN from a license issued to: "}

nl = {
    "E001": "Onjuiste structuur: De lengte van de GTIN is niet correct.",
    "E002": "Onjuiste structuur: Niet correct controle getal.",
    "E003": "Onjuiste structuur: De GTIN bevat alfanumerieke karakters.",
    "E004": "Onjuist nummer. Deze GS1 prefix(3-cijferige landcode) bestaat niet.",
    "E005": "Onjuist nummer: deze GS1 prefix is gereserveerd voor speciale toepassingen.",
    "E006": "Onjuist nummer: deze GS1 bedrijfs-prefix is niet toegekend.",
    "S001": "Onbekend nummer, er kan geen informatie gegeven worden.",
    "S002": "Onbekende GTIN van een licentie verleend aan: ",
    "S003": "Actieve GTIN van een licentie verleend aan: ",
    "S004": "Inactieve GTIN van een licentie verleend aan: ",
    "S005": "Actieve GTIN van een licentie verleend aan: "}
    


# Dictionary with the available languages
languages = {"de": de,"en": en,"nl": nl}
