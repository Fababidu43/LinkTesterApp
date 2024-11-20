; Script Inno Setup Corrigé
[Setup]
AppName=LinkTesterApp
AppVersion={#VERSION}  ; Placeholder pour la version
DefaultDirName={pf}\LinkTesterApp
DefaultGroupName=LinkTesterApp
OutputBaseFilename=setup_LinkTesterApp_v{#VERSION}  ; Inclure la version dans le nom de fichier
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\LinkTesterApp.exe"; DestDir: "{app}"; Flags: ignoreversion restartreplace

[Icons]
Name: "{group}\LinkTesterApp"; Filename: "{app}\LinkTesterApp.exe"

[Run]
Filename: "{app}\LinkTesterApp.exe"; Description: "Lancer LinkTesterApp"; Flags: nowait postinstall skipifsilent
