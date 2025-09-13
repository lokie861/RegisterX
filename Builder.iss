; Inno Setup Script to install RegisterX (Flutter UI + Python Backend)

[Setup]
; App details
AppName=RegisterX
AppVersion=1.0
AppPublisher=Lokesh
AppPublisherURL=https://github.com/lokie861
AppSupportURL=mailto:plokesh23.01@gmail.com
AppUpdatesURL=https://github.com/lokie861/RegisterX
DefaultDirName=C:\RegisterX
DefaultGroupName=RegisterX
OutputDir=Builds\Installer
OutputBaseFilename=RegisterX_Installer
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin

[Files]
; Include only EXEs from build folder
Source: "Builds\EXE\*.exe"; DestDir: "{app}"; Flags: ignoreversion
; Include configuration file
Source: "app.ini"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Start Menu shortcut
Name: "{group}\RegisterX"; Filename: "{app}\RegisterX.exe"
; Desktop shortcut
Name: "{commondesktop}\RegisterX"; Filename: "{app}\RegisterX.exe"; Tasks: desktopicon
; Auto-start backend (adjust if separate backend.exe exists)
Name: "{userstartup}\RegisterX"; Filename: "{app}\RegisterX.exe"

[Tasks]
; Extra tasks user can pick during install
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"

[Run]
; Optionally start the app after install
Filename: "{app}\RegisterX.exe"; Description: "Launch RegisterX"; Flags: nowait skipifsilent postinstall
