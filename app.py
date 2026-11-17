import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Active Vision – 5-Jahres-Marketingsimulation", layout="wide")

PRODUKT = "Active Vision – Smarte Ski- & Freeride-Brille (Basis Ski / Pro Freeride)"
JAHRE = [1, 2, 3, 4, 5]

# ---------------------------------------------------------------------------
# Konstanten (aus der Kalkulation Active Vision)
# ---------------------------------------------------------------------------
ANTEIL_PRO = 0.30
LISTENPREIS_BASIS, LISTENPREIS_PRO = 949.99, 1449.99
HERSTELL_BASIS, HERSTELL_PRO = 276.0, 339.0
SATELLIT_PRO = 45.0
CLOUD = 2.0
VERSAND = 0.8 * 15 + 0.2 * 35           # 19 €
RETOUREN = 0.08 * 40                    # 3,20 €
ZAHLUNG = 0.015
VERSAND_BRUENDL = 2.0
HANDELSSPANNE = 0.30
BUERO = 80 * 28 * 12 * 1.2              # 32.256 €
TEAM = 4 * 55000
LAGER = 24000
SHOP_AUFBAU = 15000
SHOP_BETRIEB = 6000
TESTDISPLAYS = 5 * 1500

LISTENPREIS_MIX = (1 - ANTEIL_PRO) * LISTENPREIS_BASIS + ANTEIL_PRO * LISTENPREIS_PRO
STUECKKOSTEN_MIX = (1 - ANTEIL_PRO) * HERSTELL_BASIS + ANTEIL_PRO * HERSTELL_PRO
LAUFEND_MIX = ANTEIL_PRO * SATELLIT_PRO + CLOUD

# Annahmen für die Simulation
QUALITAET = {
    "Standard": {"kosten": 1.00, "nachfrage": 1.00, "preisreferenz": 1.00},
    "Premium": {"kosten": 1.15, "nachfrage": 1.10, "preisreferenz": 1.08},
    "Luxus": {"kosten": 1.35, "nachfrage": 1.15, "preisreferenz": 1.15},
}
ELASTIZITAET = 1.6
BASIS_NACHFRAGE = 1700      # Einheiten/Jahr bei Referenzbedingungen
MARKT_GESAMT = 12000        # Marktpotenzial über 5 Jahre (Sättigung)
MARKT_REICHWEITE = {"online": 0.50, "stationaer": 0.30, "markt": 0.20}
MARKTPLATZ_PROVISION = 0.15
MARKTPLATZ_FIX = 3000
RATENZAHLUNG_NACHFRAGE = 1.08
RATENZAHLUNG_GEBUEHR = 0.015
MARKEN_ABKLINGEN = 0.75
KOSTENDEGRESSION = 0.03


def sat(x, ref):
    return 1 - np.exp(-x / ref)


def simuliere(p):
    q = QUALITAET[p["qualitaet"]]
    ref_preis = LISTENPREIS_MIX * 0.95 * q["preisreferenz"]
    preis_netto = p["preis"] * (1 - p["rabatt"] / 100)
    preisfaktor = (preis_netto / ref_preis) ** (-ELASTIZITAET)

    reichweiten = {
        "online": MARKT_REICHWEITE["online"] if p["online"] else 0.0,
        "stationaer": MARKT_REICHWEITE["stationaer"] if p["stationaer"] else 0.0,
        "markt": MARKT_REICHWEITE["markt"] if p["markt"] else 0.0,
    }
    reichweite = 1 - np.prod([1 - r for r in reichweiten.values()])
    summe_r = sum(reichweiten.values())
    anteile = {k: (v / summe_r if summe_r > 0 else 0.0) for k, v in reichweiten.items()}

    sofort = (
        1
        + 0.60 * sat(p["ads"], 30000)
        + 0.25 * sat(p["tv"], 60000)
        + 0.15 * sat(p["sponsoring"], 87000)
    )
    marken_input = (
        p["content"] + 0.6 * p["sponsoring"] + 0.3 * p["tv"] + 0.8 * p["fe"] + 0.4 * p["packaging"]
    ) / 100000
    ratenfaktor = RATENZAHLUNG_NACHFRAGE if p["raten"] else 1.0
    zahlung = ZAHLUNG + (RATENZAHLUNG_GEBUEHR if p["raten"] else 0.0)

    promotion = p["content"] + p["ads"] + p["sponsoring"] + p["tv"]
    produkt_fix = p["fe"] + p["packaging"]

    zeilen = []
    marke = 0.0
    kumuliert = 0.0
    for j in JAHRE:
        marke_wirksam = MARKEN_ABKLINGEN * marke + 0.4 * marken_input
        marke = MARKEN_ABKLINGEN * marke + marken_input
        markenfaktor = 1 + 0.9 * (1 - np.exp(-marke_wirksam / 3))
        saettigung = max(0.05, 1 - kumuliert / MARKT_GESAMT)

        absatz = (
            BASIS_NACHFRAGE * reichweite * preisfaktor * q["nachfrage"]
            * ratenfaktor * sofort * markenfaktor * saettigung
        )
        absatz = max(0.0, absatz)
        kumuliert += absatz

        umsatz = absatz * preis_netto

        stueckkosten = (
            STUECKKOSTEN_MIX * q["kosten"] * (1 - KOSTENDEGRESSION) ** (j - 1) + LAUFEND_MIX
        )
        produktion = absatz * stueckkosten + produkt_fix

        n_on, n_st, n_mk = (absatz * anteile[k] for k in ("online", "stationaer", "markt"))
        vertrieb = (
            (n_on + n_mk) * (VERSAND + RETOUREN)
            + n_st * VERSAND_BRUENDL
            + (n_on + n_mk) * preis_netto * zahlung
            + n_st * preis_netto * HANDELSSPANNE
            + n_mk * preis_netto * MARKTPLATZ_PROVISION
        )
        fix_place = BUERO + TEAM + LAGER
        if p["online"]:
            fix_place += SHOP_BETRIEB + (SHOP_AUFBAU if j == 1 else 0)
        if p["stationaer"] and j == 1:
            fix_place += TESTDISPLAYS
        if p["markt"]:
            fix_place += MARKTPLATZ_FIX
        vertrieb += fix_place

        kosten = produktion + vertrieb + promotion
        zeilen.append(
            {
                "Jahr": j,
                "Absatz (Stück)": absatz,
                "Umsatz (€)": umsatz,
                "Produktionskosten (€)": produktion,
                "Vertriebskosten (€)": vertrieb,
                "Marketingkosten (€)": promotion,
                "Gesamtkosten (€)": kosten,
                "Gewinn EBIT (€)": umsatz - kosten,
            }
        )
    return pd.DataFrame(zeilen)


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
st.sidebar.title("Parameter")

with st.sidebar.expander("1. Product", expanded=True):
    fe = st.slider("F&E-Budget (€/Jahr)", 0, 300000, 90000, 5000)
    qualitaet = st.selectbox("Materialqualität", list(QUALITAET.keys()))
    packaging = st.slider("Packaging & Design (€/Jahr)", 0, 100000, 10000, 1000)

with st.sidebar.expander("2. Price", expanded=True):
    preis = st.slider("Verkaufspreis netto (€)", 600.0, 1800.0, round(LISTENPREIS_MIX, 2), 10.0)
    rabatt = st.slider("Rabattaktionen (%)", 0, 30, 5, 1)
    raten = st.checkbox("Ratenzahlung anbieten", value=False)

with st.sidebar.expander("3. Place", expanded=True):
    online = st.checkbox(
        "Onlineshop (Aufbau 15.000 €, Betrieb 6.000 €/Jahr, Versand & Zahlungsgebühren)", value=True
    )
    stationaer = st.checkbox(
        "Stationärer Handel / On-Site-Shop (Testdisplays 7.500 €, Handelsspanne 30 %)", value=True
    )
    markt = st.checkbox(
        "Marktplätze (Fixkosten 3.000 €/Jahr, Provision 15 %)", value=False
    )

with st.sidebar.expander("4. Promotion", expanded=True):
    content = st.slider("Social Media Content (€/Jahr)", 0, 100000, 15000, 1000)
    ads = st.slider("Social Media Ads (€/Jahr)", 0, 150000, 25000, 1000)
    sponsoring = st.slider("Sponsoring / Influencer (€/Jahr)", 0, 200000, 87000, 1000)
    tv = st.slider("TV / Klassische Werbung (€/Jahr)", 0, 200000, 60000, 1000)
    teilsumme = content + ads + sponsoring + tv
    st.metric("Teilsumme Promotion (€/Jahr)", f"{teilsumme:,.0f} €".replace(",", "."))

params = dict(
    fe=fe, qualitaet=qualitaet, packaging=packaging,
    preis=preis, rabatt=rabatt, raten=raten,
    online=online, stationaer=stationaer, markt=markt,
    content=content, ads=ads, sponsoring=sponsoring, tv=tv,
)
df = simuliere(params)

# ---------------------------------------------------------------------------
# Hauptbereich
# ---------------------------------------------------------------------------
st.title("5-Jahres-Marketingsimulation")
st.caption(PRODUKT)


def eur(x):
    return f"{x:,.0f} €".replace(",", ".")


umsatz5 = df["Umsatz (€)"].sum()
gewinn5 = df["Gewinn EBIT (€)"].sum()
absatz5 = df["Absatz (Stück)"].sum()
rendite = gewinn5 / umsatz5 * 100 if umsatz5 > 0 else 0.0

k1, k2, k3, k4 = st.columns(4)
with k1:
    with st.container(border=True):
        st.metric("5J-Umsatz", eur(umsatz5))
with k2:
    with st.container(border=True):
        st.metric("5J-Gewinn (EBIT)", eur(gewinn5))
with k3:
    with st.container(border=True):
        st.metric("Absatzmenge (5J)", f"{absatz5:,.0f} Stück".replace(",", "."))
with k4:
    with st.container(border=True):
        st.metric("Umsatzrendite", f"{rendite:.1f} %".replace(".", ","))

st.subheader("Umsatz, Kosten und Gewinn")
linie = df.set_index("Jahr")[["Umsatz (€)", "Gesamtkosten (€)", "Gewinn EBIT (€)"]]
st.line_chart(linie)

st.subheader("Kostenstruktur nach Teilsummen")
kosten = df.set_index("Jahr")[["Produktionskosten (€)", "Vertriebskosten (€)", "Marketingkosten (€)"]]
st.bar_chart(kosten, stack=True)

st.subheader("Jahrestabelle")
tabelle = df.set_index("Jahr")
st.dataframe(
    tabelle.style.format(
        {c: "{:,.0f}" for c in tabelle.columns}, thousands="."
    ),
    use_container_width=True,
)
