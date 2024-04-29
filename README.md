# Ohjelmistotekniikka, harjoitustyö

Sovellus on tarkoitettu käytettäväksi yhdistyksen jäsenrekisterinä. Sovelluksessa on mahdollista lisätä, poistaa ja muokata jäseniä. Jäseniä voi hakea nimen perusteella. Sovellus on toteutettu Pythonilla ja se tallentaa jäsenet SQLite-tietokantaan. Sovellus on tehty osana Helsingin yliopiston Ohjelmistoteknikka-kurssia.

## Dokumentaatio

- [Vaatimusmäärittely](dokumentaatio/vaatimusmaarittely.md)
- [Tuntikirjanpito](dokumentaatio/tuntikirjanpito.md)
- [Changelog](dokumentaatio/changelog.md)
- [Arkkitehtuuri](dokumentaatio/arkkitehtuuri.md)

## Asennus

2. Asenna riippuvuudet komennolla `poetry install`
3. Suorita sovellus komennolla `poetry run invoke start`
4. Esimerkkidataa voi lisätä komennolla `poetry run invoke create sample data`

## Komentorivitoiminnot

### Ohjelman suorittaminen

Ohjelman voi suorittaa komennolla `poetry run invoke start`

### Testaus

Testit voi suorittaa komennolla `poetry run invoke test`

### Testikattavuus

Testikattavuusraportin voi generoida komennolla `poetry run invoke coverage-report`

### Github release

Github release löydyy osoitteesta https://github.com/nlinnanen/ot-harjoitustyo/releases/tag/viikko6
