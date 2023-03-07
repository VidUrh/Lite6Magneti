# Možni predlogi za UR aplikacijo

## Podajalec

Podajalec ohišij je lahko "feeder" in pošilja ohišja kar direktno v robotov gripper. Podobno kot prikazano na povezavi [YouTube - Screw feeder](https://youtube.com/shorts/93dVMB96Kgs?feature=share)

|                     	| +                           	| -                                                                                                            	 |
|---------------------	|-----------------------------	|--------------------------------------------------------------------------------------------------------------	 |
| Uporaba vibratorja   	| + enostavnost izvedbe       	| - Počasen <br> - Človek polni zalogovnik                                                                     	 | 
| Feeder (direktno na tcp) | + hitrost (manj gibov) <br> 	| - Možne težave ker mora biti cevka vedno povezana na vrh robota<br>- Težave ker je treba magnet obrniti navzgor <br>3- Dodatna komponenta, višja cena <br>- Čas dobavljivosti je vprašljiv| 
| Pobiranje iz škatel 	| + Brez vibratorja <br>+ Cenejša izvedba 	| - Zahtevnejša in počasnejša implementacija                                                                   	 |

## Izvedba z rotacijskim vibratorjem
### Pozicija ohišja
Ohišje je lahko obrnjeno z špico navzgor ali navzdol. Predpostavimo da dispenzer nesmemo obračati.

|                     	| +                           	| -                                                                                                            	 |
|---------------------	|-----------------------------	|--------------------------------------------------------------------------------------------------------------	 |
| Navzgor     | + Lažje prijemanje       	| - nepotrebno obračanje robota <br> - počasnejši cikel | 
| Navzdol     | + Manj obračanja <br> + Krajši cikel         	| - Težje prijemanj |

## Pobiranje magnetov
Ena izmed opcije je tudi, da robot pobira magnete.
To bi bilo izvedljivo z nekakšnim dvojnim gripperjem.
Koraki ideje:
  1. Robot pobere ohišje oz. mu ga dostavi feeder
  2. Nanos lepila na ohišje
  3. Pobere magnet (magnet bi bi la griperju nameščen tik nad ohišjem, tako da bi bil že pozicioniran na luknjo)
  4. Robot se prestavi na magnetno ploščo in se ji približa.
  5. Tik nad ploščo spusti magnet in istočasno pritisne ohišje do plošče.

Pri tej izvedbi je velika prednost v tem da je magnet že pozicionitan točno pod luknjo ohišja, saj ga tam spusti gripper.

## Prvi prototip in testi
Z uFactory lite 6 robotom sva naredila program in test, za zgoraj omenjeni rotaciji ohišja.

Čas cikla:
  - navzgor 8,5 s (daljša pot zaradi rotacije ohišja za 180°)
  - navzdol 7,3 s
  - navzdol + dispenzeer nad ohišji 5,2 s
  - '+ pobiranje magnetov 9 s
  - '+ brisanje po 30 min

V tem ciklu je samo pobiranje, lepljenje in postavljanje ohišja na magnet (brez brisanja in dodatnih del)
