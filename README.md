# OnlySport - Web-sovellus

## Sovelluksen tarkoitus

OnlySport on verkkosovellus ihmisille, jotka yksinkertaisesti rakastavat urheilua ja dataa. Käyttäjä voi tehdä sovellukseen tilin, jolloin hän voi tallentaa sovellukseen urheilusuorituksiaan sekä tarkastella muiden käyttäjien urheilusuorituksia.

## Sovelluksen toiminnallisuus

- [x] Rekisteröityminen, kirjautuminen, käyttäjäasetusten muuttaminen ja tilin poistaminen
- [x] Urheilusuoritusten lisääminen, tarkastelu ja poistaminen
- [x] Urheilusuoritusten luokittelu (esim. fiilis, kuormittavuus)
- [x] Urheilusuoritusten hakeminen lajin tai kuvauksen perusteella
- [x] Muiden käyttäjien urheilusuoritusten tarkastelu
- [x] Urheilusuoritusten kommentointi
- [ ] Tykkäysten antaminen muiden käyttäjien urheilusuorituksille
- [x] Tilastotietojen tarkastelu urheilusuorituksista käyttäjäsivulla

## Käyttöohjeet sovelluksen testaamiseen

> [!NOTE]
> Sovelluksen testaaminen vaatii, että tietokoneelle on asennettu python3 ja pip.

Kloonaa projekti omalle tietokoneelle:
```
$ git clone https://github.com/ronjass/tikawe-sport.git
```
Navigoi projektihakemiston juureen ja luo projektille virtuaaliympäristö komennolla:
```
$ python3 -m venv venv
```
Käynnistä virtuaaliympäristö komennolla:
```
$ source venv/bin/activate
```
Asenna Flask virtuaaliympäristöön komennolla:
```
$ pip install flask
```
Alusta tietokannat komennoilla:
```
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```
Käynnistä sovellus komennolla:
```
$ flask --app onlysport run
```
