Erstelle mir den vollständigen Python-Code für eine interaktive Streamlit-Web-App (app.py), die eine detaillierte 5-Jahres-Marketingsimulation für unser Produkt abbildet.

PRODUKT: Active Vision, eine digitale Skibrille mit interaktiver, kostenloser App, entwickelt in Kooperation mit Oakley (weiterer Partner: Ski Amadé).
File "/mount/src/marketing-sim-gruppe2/app.py", line 4
- Basis (Ski): Kamera, Pisteninfo, Pulsmessung, GPS, Mikro-Display, Ladecase
- Pro (Freeride): zusätzlich Magnetometer (Richtungspfeil), Satellitenmodul (SOS), Link-up-Funk (Brille zu Brille)
- Zielgruppe: 15 bis 50 Jahre (Freerider, Skilehrer, erfahrene Skifahrer)
- Herstellkosten pro Brille: Basis 276 €, Pro 339 €
- Einmalige Produktkosten (nur Jahr 1): 450.000 € (Entwicklung/Design 200.000, Werkzeuge 80.000, Zertifizierungen 50.000, App 120.000)
- Laufend pro Nutzer und Jahr: Cloud 2 € (alle Nutzer), Satellitendienst 45 € (nur Pro). Diese Kosten fallen für den gesamten Nutzerbestand an, also für alle seit Jahr 1 verkauften Brillen.
- Oakley-Lizenz: noch offen, derzeit mit 0 € angesetzt

PRICE (alle Preise netto, Österreich, USt 20 %):
- Listenpreis: Basis 949,99 € (brutto 1.139,99 €), Pro 1.449,99 € (brutto 1.739,99 €)
- Rabatte: Ski Amadé (Basis -10 %, Pro -15 %), Launch (-5 % nur in Jahr 1), Buddy (nur Pro, -150 €). Im Durchschnitt ergibt das ca. 5 % Rabatt.
- Gewinn pro Brille im Direktverkauf ohne Rabatt: Basis 635,54 €, Pro 1.020,04 €
- Gewinn pro Brille mit Ski Amadé + Launch: Basis 499,86 €, Pro 745,10 €

PLACE:
- Online-Direktvertrieb und Bründl-Sports-Filialen (Handelsspanne ca. 30 %), Versand DHL (80 %) und FedEx (20 %)
- Variable Kosten pro Brille im Direktverkauf: Versand 19 €, Retouren 3,20 €, Zahlungsgebühren 1,5 % vom Preis. Beim Verkauf über Bründl entfallen diese Kosten, dort gelten nur 2 € Sammelversand pro Brille.
- Fixkosten Place: 304.756 € pro Jahr, davon Basis-HQ 276.256 € (Büro Frankfurt 32.256, HQ-Team 220.000, Lager 24.000), Online-Shop 21.000 € (Aufbau 15.000 + Betrieb 6.000), 5 Testdisplays bei Bründl 7.500 €

PROMOTION (gesamt 187.000 € pro Jahr):
Social Media Content 15.000, Social Media Ads 25.000, Profisportler (mit Oakley) 30.000, Skischulen 12.000, Ski Amadé 20.000, Testfahrten bei Bründl 10.000, Skirennen-Sponsoring 15.000, TV-Spot Sportsender 60.000.

KALIBRIERUNG (Jahr 1 mit Standardwerten, soll ungefähr so herauskommen):
- 2.000 Brillen (70 % Basis, 30 % Pro), Verkauf komplett online
- Ø Nettopreis nach Rabatten: 1.045,36 €, Umsatz ca. 2.090.721 €
- Fixkosten gesamt: 941.756 €, Gewinn (EBIT) ca. 452.405 € (Marge ca. 21,6 %)
- Break-even: ca. 1.352 Brillen

AUFBAU DER SEITENLEISTE (Sidebar) in 4 aufklappbaren Sektionen (st.expander):
1. Product: Slider für F&E-Budget (€/Jahr, Standard 200.000), Slider für den Anteil Pro in % (Standard 30), Auswahlfeld Materialqualität (Standard, Premium, Luxus; Standard entspricht den Herstellkosten oben, Premium und Luxus erhöhen Stückkosten und Nachfrage), Slider für Packaging & Design (€/Jahr, Standard 0, da die Verpackung bereits in den Herstellkosten steckt). Die übrigen einmaligen Kosten (Werkzeuge, Zertifizierungen, App = 250.000 €) fallen fix nur in Jahr 1 an.
2. Price: Slider für den Verkaufspreis (€) getrennt für Basis und Pro, Slider für Rabattaktionen in % (Standard 5), Checkbox für Ratenzahlung (erhöht die Nachfrage, kostet Finanzierungsgebühr/Zahlungsausfälle).
3. Place: Checkboxen für Onlineshop, Stationärer Handel (Bründl Sports) und Marktplätze (inkl. Fixkosten und Provisionen; für Marktplätze plausible Annahmen treffen und im Code kennzeichnen). Das Basis-HQ (276.256 €/Jahr) fällt immer an.
4. Promotion (mit Live-Teilsumme): Einzelne Slider für Social Media Content, Social Media Ads, Profisportler/Sponsoring, Skischulen, Ski Amadé, Testfahrten und Skirennen-Sponsoring sowie TV-Spot (€/Jahr, Standardwerte wie oben). Zeige die Teilsumme Promotion (€/Jahr) live an.

SIMULATIONSLOGIK (Jahr 1 bis 5) UND VISUALISIERUNG:
- Berechne Absatz, Umsatz, Produktions-, Vertriebs- und Marketingkosten sowie Gewinn (EBIT) über 5 Jahre.
- Berücksichtige Preiselastizität, Sofortwirkung (Ads, TV, Skirennen) gegenüber langfristigem Markenaufbau (Content, Sponsoring, Ski Amadé, F&E mit Carry-over und Abklingrate) und Marktsättigung (begrenztes Marktpotenzial, abnehmende Grenzerträge der Werbung). Alle Annahmen als Konstanten am Anfang des Codes dokumentieren.
- Launch-Rabatt gilt nur in Jahr 1. Recurring-Kosten (Cloud, Satellitendienst) laufen auf dem Nutzerbestand.
- Mit den Standardwerten soll Jahr 1 die Kalibrierung oben ungefähr treffen.
- Zeige oben 4 KPI-Karten (5J-Umsatz, 5J-Gewinn, Absatzmenge gesamt, Umsatzrendite %), darunter ein Liniendiagramm (Umsatz/Kosten/Gewinn), ein gestapeltes Balkendiagramm (Kostenstruktur nach Teilsummen) und eine Jahrestabelle.
- Zahlen im deutschen Format (1.234,56 €), alle Texte auf Deutsch.
- Nutze ausschließlich streamlit, pandas und numpy. Der Code soll vollständig, kommentiert und direkt mit "streamlit run app.py" lauffähig sein.
