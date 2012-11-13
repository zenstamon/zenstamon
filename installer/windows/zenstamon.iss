; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "Zenstamon"
#define MyAppVersion ".2"
#define MyAppExeName "zenstamon.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{A686585D-89D9-4DED-AAD6-0F15051D8F23}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
DefaultDirName={sd}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputBaseFilename=Zenstamon_.2_setup
SetupIconFile=C:\zenstamon\dist\zenstamon\resources\zenstamon.ico
InternalCompressLevel=max
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}";
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 0,6.1
Name: "autostart"; Description: "Enable Auto Start on Login"; GroupDescription: "{cm:AdditionalIcons}";


[Files]
Source: "C:\zenstamon\dist\zenstamon\zenstamon.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\zenstamon\dist\zenstamon\_hashlib.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\zenstamon\dist\zenstamon\_socket.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\zenstamon\dist\zenstamon\_ssl.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\zenstamon\dist\zenstamon\bz2.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\zenstamon\dist\zenstamon\Microsoft.VC90.CRT.manifest"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\zenstamon\dist\zenstamon\msvcm90.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\zenstamon\dist\zenstamon\msvcp90.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\zenstamon\dist\zenstamon\msvcr90.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\zenstamon\dist\zenstamon\PyQt4.QtCore.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\zenstamon\dist\zenstamon\PyQt4.QtGui.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\zenstamon\dist\zenstamon\python27.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\zenstamon\dist\zenstamon\QtCore4.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\zenstamon\dist\zenstamon\QtGui4.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\zenstamon\dist\zenstamon\QtOpenGL4.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\zenstamon\dist\zenstamon\QtSvg4.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\zenstamon\dist\zenstamon\QtXml4.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\zenstamon\dist\zenstamon\select.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\zenstamon\dist\zenstamon\sip.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\zenstamon\dist\zenstamon\unicodedata.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\zenstamon\dist\zenstamon\zenstamon.exe.manifest"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\zenstamon\resources\*"; DestDir: "{app}\resources"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\zenstamon\dist\zenstamon\qt4_plugins\*"; DestDir: "{app}\qt4_plugins"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon
Name: "{userstartup}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}";WorkingDir: {app}; Tasks: autostart


[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[code]
function NextButtonClick(CurPageID: Integer): Boolean;
var
  Index: Integer;
begin
  Result := True;
  if CurPageID = wpSelectTasks then
  begin
    Index := WizardForm.TasksList.Items.IndexOf('Task Description');
    if Index <> -1 then
    begin
      if WizardForm.TasksList.Checked[Index] then
        MsgBox('First task has been checked.', mbInformation, MB_OK)
      else
        MsgBox('First task has NOT been checked.', mbInformation, MB_OK);
    end;
  end;
end;

procedure CurPageChanged(CurPageID: Integer);
var
  Index: Integer;
begin
  if CurPageID = wpSelectTasks then
  begin
    Index := WizardForm.TasksList.Items.IndexOf('Task Description');
    if Index <> -1 then    
      WizardForm.TasksList.Checked[Index] := False;
  end;
end;   

