# OnlySport - Web-sovellus

## Sovelluksen tarkoitus

OnlySport on verkkosovellus ihmisille, jotka yksinkertaisesti rakastavat urheilua ja dataa. Sovelluksen perusideana on, että kirjautuneet käyttäjät voivat tallentaa sivustolle urheilusuorituksiaan. Sovellus tuo urheilua rakastavat ihmiset yhteen, sillä sovelluksessa voi tarkastella muiden lisäämiä urheilusuorituksia, ja lisäksi kirjautuneet käyttäjät voivat kommentoida urheilusuorituksia ja tykätä niistä.

## Sovelluksen toiminnallisuus

✅ Rekisteröityminen, kirjautuminen ja tilin poistaminen

✅ Urheilusuoritusten lisääminen, tarkastelu ja poistaminen

✅ Urheilusuoritusten luokittelu (esim. fiilis, kuormittavuus)

✅ Urheilusuoritusten hakeminen lajin tai kuvauksen perusteella

✅ Muiden käyttäjien urheilusuoritusten tarkastelu

✅ Urheilusuoritusten kommentointi

✅ Tykkäysten antaminen urheilusuorituksille

✅ Tilastotietojen tarkastelu urheilusuorituksista käyttäjäsivulla

✅ Profiilikuvan lisääminen ja poistaminen käyttäjäsivuilla

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
$ flask run
```
