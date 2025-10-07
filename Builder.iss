; Inno Setup Script to install RegisterX (Flutter UI + Python Backend)
[Setup]
; App details
PrivilegesRequired=admin
AppName=RegisterX
AppVersion=0.1.1
AppPublisher=Lokesh
AppPublisherURL=https://github.com/lokie861
AppSupportURL=mailto:plokesh23.01@gmail.com
AppUpdatesURL=https://github.com/lokie861/RegisterX
DefaultDirName={userpf}\RegisterX
DefaultGroupName=RegisterX
AppMutex=RegisterX_SingleInstanceMutex
OutputDir=Builds\Installer
OutputBaseFilename=RegisterX_Installer
Compression=lzma
SolidCompression=yes
AppId={{B7E8F4A2-6D3C-4B9E-8F1A-2C5D7E9F0B1C}}
UninstallDisplayName=RegisterX
UninstallDisplayIcon={app}\RegisterX.exe
CreateUninstallRegKey=yes


[Files]
; Include only EXEs from build folder
Source: "Builds\EXE\*.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\RegisterX"; Filename: "{app}\RegisterX.exe"; WorkingDir: "{app}"
Name: "{userdesktop}\RegisterX"; Filename: "{app}\RegisterX.exe"; WorkingDir: "{app}"; Tasks: desktopicon

[Registry]
; Startup entry (already exists under HKCU)
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; \
    ValueName: "RegisterX"; ValueType: string; ValueData: """{app}\RegisterX.exe"""; Flags: uninsdeletevalue;

; Create parent key (no value needed, just ensures it exists)
Root: HKCU; Subkey: "SOFTWARE\RegisterX"; Flags: uninsdeletekeyifempty

; Now add defaults only if missing
Root: HKCU; Subkey: "SOFTWARE\RegisterX"; ValueType: string; ValueName: "host"; ValueData: "127.0.0.1"; Flags: uninsdeletevalue createvalueifdoesntexist
Root: HKCU; Subkey: "SOFTWARE\RegisterX"; ValueType: string; ValueName: "port"; ValueData: "7000"; Flags: uninsdeletevalue createvalueifdoesntexist
Root: HKCU; Subkey: "SOFTWARE\RegisterX"; ValueType: string; ValueName: "run_systray"; ValueData: "true"; Flags: uninsdeletevalue createvalueifdoesntexist
Root: HKCU; Subkey: "SOFTWARE\RegisterX"; ValueType: string; ValueName: "debug"; ValueData: "false"; Flags: uninsdeletevalue createvalueifdoesntexist
Root: HKCU; Subkey: "SOFTWARE\RegisterX"; ValueType: string; ValueName: "version"; ValueData: "0.2.2"; Flags: uninsdeletevalue

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"
; Name: "startup"; Description: "Start RegisterX when Windows starts"; GroupDescription: "Startup options:"

[Run]
; Optionally start the app after install
Filename: "{app}\RegisterX.exe"; Description: "Launch RegisterX"; Flags: postinstall skipifsilent nowait; WorkingDir: "{app}"

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

function GetUninstallString(): string;
var
  sUnInstPath: string;
  sUnInstallString: string;
begin
  sUnInstPath := 'Software\Microsoft\Windows\CurrentVersion\Uninstall\{#SetupSetting("AppId")}_is1';
  sUnInstallString := '';
  // Only check HKCU since we're using lowest privileges
  RegQueryStringValue(HKCU, sUnInstPath, 'UninstallString', sUnInstallString);
  Result := sUnInstallString;
end;

function IsUpgrade(): Boolean;
begin
  Result := (GetUninstallString() <> '');
end;

function UnInstallOldVersion(): Integer;
var
  sUnInstallString: string;
  iResultCode: Integer;
begin
  Result := 0;
  sUnInstallString := GetUninstallString();
  if sUnInstallString <> '' then begin
    sUnInstallString := RemoveQuotes(sUnInstallString);
    if Exec(sUnInstallString, '/SILENT /NORESTART /SUPPRESSMSGBOXES','', SW_HIDE, ewWaitUntilTerminated, iResultCode) then
      Result := 3
    else
      Result := 2;
  end else
    Result := 1;
end;

// Create a batch file to ensure proper working directory
procedure CreateStartupBatch();
var
  BatchContent: string;
  BatchPath: string;
begin
  BatchPath := ExpandConstant('{app}\RegisterX_Startup.bat');
  BatchContent := 
    '@echo off' + #13#10 +
    'cd /d "%~dp0"' + #13#10 +
    'start "" "RegisterX.exe"' + #13#10;
  
  SaveStringToFile(BatchPath, BatchContent, False);
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if (CurStep = ssInstall) then
  begin
    if (IsUpgrade()) then
    begin
      UnInstallOldVersion();
      // Wait for uninstallation to complete
      Sleep(2000);
    end;
  end;
  
  if (CurStep = ssPostInstall) then
  begin
    // Create startup batch file
    CreateStartupBatch();
  end;
end;

function InitializeSetup(): Boolean;
var
  Response: Integer;
  OldVersionFound: Boolean;
begin
  Result := True;
  OldVersionFound := IsUpgrade();
  
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
        Exit;
      end;
    end
    else
    begin
      // User chose not to close the app
      Result := False;
      Exit;
    end;
  end;
  
  // Handle old installation
  if OldVersionFound then
  begin
    Response := MsgBox('A previous version of RegisterX was detected on your system.' + #13#13 +
                       'The installer will automatically remove the old version before installing the new one.' + #13#13 +
                       'Click "Yes" to continue with the upgrade.' + #13 +
                       'Click "No" to cancel the installation.',
                       mbConfirmation, MB_YESNO);
    if Response = IDNO then
    begin
      Result := False;
      Exit;
    end;
  end;
end;

// Function to check and close app before uninstall
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
      
    // Clean up any remaining registry entries (HKCU only)
    RegDeleteKeyIncludingSubkeys(HKCU, 'Software\Microsoft\Windows\CurrentVersion\Uninstall\{#SetupSetting("AppId")}_is1');
    
    // Remove startup entry if it exists
    RegDeleteValue(HKCU, 'Software\Microsoft\Windows\CurrentVersion\Run', 'RegisterX');
  end;
end;