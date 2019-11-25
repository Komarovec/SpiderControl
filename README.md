# SpiderControl
Control your robotic spider via BLE using your voice of keyboard.

# Spuštění
Aplikace je testovaná pouze na MS Windows! 
*Všechny knihovny jsou sice podporovány i na Linux, ale funkčnost nebyla testována.*\n
Doporučená verze interpreteru Python 3.6 a vyšší.\n
Následující příkazy proveďte v příkazovém řádku cmd nebo v MS PowerShell.\n
\n
1) Po rozbalení či naklonování repozitáře vstupte do složky, ve které se nachází python skripty.\n
\n
2) Ve virtuální prostředí nebo v globální instalaci nejprve nainstalujeme všechny požadavky, definované v souboru requirements.txt:\n
```
pip install -r requirements.txt
```
\n
3) Jediný požadavek, který zde není definován je PyAudio a musíme ho nainstalovat zvlášť:\n
```
pipwin install pyaudio
```
\n
4) Hlavní skript by nyní měl být spustitelný:\n
```
python main.py
```
\n
# Ovládání
Ikonka vlevo nahoře indikuje připojení k Bluetoothu. (Někdy může zmizet :) )\n
Pro ovládání robota klávesnící stačí jednou stisknout klávesu odpovídající příkazu, \n
tento příkaz bude poslán přes bluetooth, alternativně se navýší hodnota "Send queue size" a čeká na připojení.\n
Keybinds:\n
- Šipka nahoru - Dopředu
- Šipka dolu - Dozadu
- Šipka doleva - Doleva
- Šipka doprava - Doprava
D - Tanec
F - Útok
Q, E - Chůze do boku
H - Mávání
NUMPAD9 - Vysoká pozice
NUMPAD6 - Střední pozice
NUMPAD3 - Nízká pozice
\n
# Hlasové ovládání
Stisknutím tlačítka "Voice Control", se aktivuje nahrávání výchozího mikrofonu a posílání k rozboru hlasu.\n
Tyto operace mají vysokou odezvu a proto nedoporučuji takto robota ovládat.\n
Nejlépe fungující příkazy:\n
- "Dance" - Tanec
- "Fight" - Útok
- "Hi/Hello" - Zamávání
\n
Ostatní:\n
- "Forward" - Chůze vpřed
- "Backward" - Chůze vzad
- "Turn left" - Otočit vlevo
- "Turn right" - Otočit vpravo
- "Stop" - Stůj
