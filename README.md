# SpiderControl
Control your robotic spider via BLE using your voice of keyboard.

# Spuštění
Aplikace je testovaná pouze na MS Windows! Všechny knihovny jsou sice podporovány i na Linux, ale funkčnost nebyla testována.
Doporučená verze interpreteru Python 3.6 a vyšší.
Následující příkazy proveďte v příkazovém řádku cmd nebo v MS PowerShell.

1) Po rozbalení či naklonování repozitáře vstupte do složky, ve které se nachází python skripty.

2) Ve virtuální prostředí nebo v globální instalaci nejprve nainstalujeme všechny požadavky, definované v souboru requirements.txt:
```
pip install -r requirements.txt
```

3) Jediný požadavek, který zde není definován je PyAudio a musíme ho nainstalovat zvlášť:
```
pipwin install pyaudio
```

4) Hlavní skript by nyní měl být spustitelný:
```
python main.py
```

# Ovládání
Ikonka vlevo nahoře indikuje připojení k Bluetoothu. (Někdy může zmizet :) )
Pro ovládání robota klávesnící stačí jednou stisknout klávesu odpovídající příkazu, 
tento příkaz bude poslán přes bluetooth, alternativně se navýší hodnota "Send queue size" a čeká na připojení.
Keybinds:
Šipka nahoru - Dopředu
Šipka dolu - Dozadu
Šipka doleva - Doleva
Šipka doprava - Doprava
D - Tanec
F - Útok
Q, E - Chůze do boku
H - Mávání
NUMPAD9 - Vysoká pozice
NUMPAD6 - Střední pozice
NUMPAD3 - Nízká pozice

# Hlasové ovládání
Stisknutím tlačítka "Voice Control", se aktivuje nahrávání výchozího mikrofonu a posílání k rozboru hlasu.
Tyto operace mají vysokou odezvu a proto nedoporučuji takto robota ovládat.
Nejlépe fungující příkazy:
"Dance" - Tanec
"Fight" - Útok
"Hi/Hello" - Zamávání
Ostatní:
"Forward" - Chůze vpřed
"Backward" - Chůze vzad
"Turn left" - Otočit vlevo
"Turn right" - Otočit vpravo
"Stop" - Stůj
