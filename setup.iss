; Script Inno Setup Corrigé pour LinkTesterApp

[Setup]
AppName=LinkTesterApp
AppVersion=1.0.0
AppId={{YOUR-GUID-HERE}}  ; Remplacez par un GUID unique
DefaultDirName={pf}\LinkTesterApp
DefaultGroupName=LinkTesterApp
OutputBaseFilename=setup_LinkTesterApp_1.0.0
Compression=lzma
SolidCompression=yes
OverwriteReadOnlyFiles=yes  ; Directive valide pour écraser les fichiers en lecture seule
PrivilegesRequired=admin     ; Nécessite les droits administrateur pour installer

[Files]
Source: "dist\LinkTesterApp.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\LinkTesterApp"; Filename: "{app}\LinkTesterApp.exe"

[Run]
Filename: "{app}\LinkTesterApp.exe"; Description: "Lancer LinkTesterApp"; Flags: nowait postinstall skipifsilent
