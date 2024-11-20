; Script Inno Setup Corrigé
[Setup]
AppName=LinkTesterApp
AppVersion=1.0.8
DefaultDirName={pf}\LinkTesterApp
DefaultGroupName=LinkTesterApp
OutputBaseFilename=setup_LinkTesterApp
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\LinkTesterApp.exe"; DestDir: "{app}"; Flags: ignoreversion restartreplace

[Icons]
Name: "{group}\LinkTesterApp"; Filename: "{app}\LinkTesterApp.exe"

[Run]
Filename: "{app}\LinkTesterApp.exe"; Description: "Lancer LinkTesterApp"; Flags: nowait postinstall skipifsilent