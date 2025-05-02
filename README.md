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

## Sovelluksen testaus suurella tietomäärällä

Projektikansiossa on mukana tiedosto seed.py, jolla voi alustaa testiaineiston komennolla:
```
$ python3 seed.py
```

Tiedosto alustaa tietokantaan testiaineiston, jossa on:

- 1000 käyttäjää
- 1000000 (miljoona) urheilusuoritusta
- 1000000 (miljoona) kommenttia
- 1000 tykkäystä jokaisessa urheilusuorituksessa

Urheilusuoritukset ovat muotoa "sport" + id-numero eli esimerkiksi "sport100". Jokaiselle urheilusuoritukselle arvotaan satunnaisesti käyttäjä, joka on lisännyt suorituksen. Lisäksi urheilusuorituksen lisätiedot (aika, matka, luokitukset) on satunnaisesti arvottu. Kommentit on nimetty suoritusten tavoin eli esimerkiksi "comment123". Jokaiselle kommentille arvotaan satunnaisesti, mihin urheilusuoritukseen se on lisätty ja mikä käyttäjä on lisännyt kommentin.

Lisäsin sovellukseen koodin, joka mittaa, kuinka nopeasti sovellus vastaa sivupyyntöihin. Ensimmäisellä testikerralla sovellus toimi hitaasti. Esimerkiksi urheilusuorituksen sport1000000 avaaminen etusivulta vie aikaa melkein 25 sekuntia ja urheilusuorituslistauksen avaaminen vie aikaa melkein sekunnin.

![alt text](https://github.com/ronjass/tikawe-sport/blob/main/media/big_data_testing.png "Sivupyyntöjen ajanmittaus ilman indeksejä")

Lisäsin tietokantaan seuraavat indeksit, jotta sovellus toimisi nopeammin:

`CREATE INDEX idx_sports_user ON sports(user_id);`

`CREATE INDEX idx_sport_comments ON comments (sport_id);`

`CREATE INDEX idx_comments_user ON comments (user_id);`

`CREATE INDEX idx_sport_likes ON likes (sport_id);`

`CREATE INDEX idx_likes_user on likes (user_id, sport_id);`

`CREATE INDEX idx_sport_classes_sport ON sport_classes (sport_id);`

Indeksien lisäämisen jälkeen sovellus toimii nopeasti. Nyt esimerkiksi urheilusuorituksen sport1000000 avaaminen etusivulta vie aikaa 0,01 sekuntia ja urheilusuorituslistan avaaminen vie aikaa 0,03 sekuntia. Indeksien avulla sovellus siis toimii nopeasti myös suurella tietomäärällä.

![alt text](https://github.com/ronjass/tikawe-sport/blob/main/media/big_data_testing_idx.png "Sivupyyntöjen ajanmittaus indekseillä")

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
