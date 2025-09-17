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
; Uninstall settings to ensure visibility in Control Panel
UninstallDisplayName=RegisterX
UninstallDisplayIcon={app}\RegisterX.exe
CreateUninstallRegKey=yes
; Optional: Add estimated size (in KB) - helps with Control Panel display
;UninstallDisplaySize=50000

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

[Registry]
; Adds app to startup if the user selects the startup task
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; \
ValueName: "RegisterX"; ValueType: string; ValueData: "{app}\RegisterX.exe"; Flags: uninsdeletevalue; Tasks: startup

; Additional registry entries to ensure proper Control Panel display
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\{#SetupSetting("AppId")}"; \
ValueType: string; ValueName: "DisplayName"; ValueData: "RegisterX"; Flags: uninsdeletekey
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\{#SetupSetting("AppId")}"; \
ValueType: string; ValueName: "DisplayVersion"; ValueData: "1.0"; Flags: uninsdeletekey
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\{#SetupSetting("AppId")}"; \
ValueType: string; ValueName: "Publisher"; ValueData: "Lokesh"; Flags: uninsdeletekey
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\{#SetupSetting("AppId")}"; \
ValueType: string; ValueName: "DisplayIcon"; ValueData: "{app}\RegisterX.exe"; Flags: uninsdeletekey
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\{#SetupSetting("AppId")}"; \
ValueType: string; ValueName: "UninstallString"; ValueData: "{uninstallexe}"; Flags: uninsdeletekey
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\{#SetupSetting("AppId")}"; \
ValueType: string; ValueName: "InstallLocation"; ValueData: "{app}"; Flags: uninsdeletekey

[Tasks]
; Extra tasks user can pick during install
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"
Name: "startup"; Description: "Start RegisterX when Windows starts"; GroupDescription: "Startup options:"

[Run]
; Optionally start the app after install
Filename: "{app}\RegisterX.exe"; Description: "Launch RegisterX"; Flags: nowait postinstall skipifsilent

[Code]
function IsAppRunning(const FileName: string): Boolean;
var
  FWMIService: Variant;
  FSWbemLocator: Variant;
  FWbemObjectSet: Variant;
begin
  Result := false;
  try
    FSWbemLocator := CreateOleObject('WBEMScripting.SWBEMLocator');
    FWMIService := FSWbemLocator.ConnectServer('', 'root\CIMV2', '', '');
    FWbemObjectSet := FWMIService.ExecQuery(Format('SELECT Name FROM Win32_Process WHERE Name="%s"',[FileName]));
    Result := (FWbemObjectSet.Count > 0);
  except
    Result := false;
  end;
end;

function KillTask(ExeFileName: string): Integer;
var
  ResultCode: Integer;
begin
  Exec('taskkill.exe', '/f /im "' + ExeFileName + '"', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
  Result := ResultCode;
end;

function InitializeSetup(): Boolean;
begin
  Result := True;
  
  // Check if RegisterX.exe is running
  if IsAppRunning('RegisterX.exe') then
  begin
    if MsgBox('RegisterX is currently running. The installer needs to close it to continue.' + #13#13 + 
              'Click "Yes" to automatically close RegisterX and continue with the installation.' + #13 +
              'Click "No" to cancel the installation.', 
              mbConfirmation, MB_YESNO) = IDYES then
    begin
      // Try to kill the process
      if KillTask('RegisterX.exe') = 0 then
      begin
        MsgBox('RegisterX has been closed successfully. The installation will now continue.', mbInformation, MB_OK);
        // Wait a moment for the process to fully terminate
        Sleep(1000);
      end
      else
      begin
        MsgBox('Failed to close RegisterX automatically. Please close the application manually and run the installer again.', mbError, MB_OK);
        Result := False;
      end;
    end
    else
    begin
      // User chose not to close the app
      Result := False;
    end;
  end;
end;

// Alternative function to check and close app before uninstall
function InitializeUninstall(): Boolean;
begin
  Result := True;
  
  // Check if RegisterX.exe is running
  if IsAppRunning('RegisterX.exe') then
  begin
    if MsgBox('RegisterX is currently running. The uninstaller needs to close it to continue.' + #13#13 + 
              'Click "Yes" to automatically close RegisterX and continue with the uninstallation.' + #13 +
              'Click "No" to cancel the uninstallation.', 
              mbConfirmation, MB_YESNO) = IDYES then
    begin
      // Try to kill the process
      if KillTask('RegisterX.exe') = 0 then
      begin
        MsgBox('RegisterX has been closed successfully. The uninstallation will now continue.', mbInformation, MB_OK);
        // Wait a moment for the process to fully terminate
        Sleep(1000);
      end
      else
      begin
        MsgBox('Failed to close RegisterX automatically. Please close the application manually and run the uninstaller again.', mbError, MB_OK);
        Result := False;
      end;
    end
    else
    begin
      // User chose not to close the app
      Result := False;
    end;
  end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usPostUninstall then
  begin
    // Remove the entire installation folder
    if DirExists(ExpandConstant('{app}')) then
      DelTree(ExpandConstant('{app}'), True, True, True);
  end;
end;