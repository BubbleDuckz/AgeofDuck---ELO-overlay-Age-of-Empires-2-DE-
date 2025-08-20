; AgeOfDuck Installer (onedir build)

#define ProjectDir "C:\Users\Parsa\Desktop\AoEDuckMod"
#define BuildDir   ProjectDir + "\dist\AgeOfDuck"

[Setup]
AppId={{E5A6C0F2-3EE7-4F22-9B7F-9E0F0B8D1A7C}}
AppName=Age of Duck MOD | AOE 2 ELO & Helper Overlay
AppVersion=1.1.4
AppPublisher=BubbleDuckz
DefaultDirName={commonpf}\AgeOfDuckOverlay
DefaultGroupName=Age of Duck MOD
UninstallDisplayIcon={app}\AgeOfDuck.exe
OutputBaseFilename=AgeOfDuckInstaller
OutputDir=.
WizardStyle=modern
Compression=lzma
SolidCompression=yes
DisableProgramGroupPage=no
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=admin
SetupIconFile={#ProjectDir}\duck.ico
UsePreviousAppDir=yes
UsePreviousLanguage=yes

CloseApplications=yes
CloseApplicationsFilter=AgeOfDuck.exe
RestartApplications=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"

[Files]
; Copy EVERYTHING from your onedir output (includes _internal, assets, exe)
Source: "{#BuildDir}\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion restartreplace

; If you keep extra loose assets outside the onedir, add them explicitly:
; Source: "{#ProjectDir}\duck.png";           DestDir: "{app}"; Flags: ignoreversion
; Source: "{#ProjectDir}\profile.png";        DestDir: "{app}"; Flags: ignoreversion
; Source: "{#ProjectDir}\civ_data.json";      DestDir: "{app}"; Flags: ignoreversion
; Source: "{#ProjectDir}\unit_counters.json"; DestDir: "{app}"; Flags: ignoreversion
; Source: "{#ProjectDir}\Units\*";            DestDir: "{app}\Units";  Flags: recursesubdirs createallsubdirs ignoreversion
; Source: "{#ProjectDir}\CivIcons\*";         DestDir: "{app}\CivIcons";Flags: recursesubdirs createallsubdirs ignoreversion

[InstallDelete]
Type: files; Name: "{app}\ageofduck_launcher.exe"
Type: files; Name: "{app}\AgeOfDuck_Launcher_Update.exe"
Type: files; Name: "{app}\launcher_updater.exe"

[Icons]
Name: "{group}\Age of Duck Overlay"; Filename: "{app}\AgeOfDuck.exe"
Name: "{commondesktop}\Age of Duck Mod"; Filename: "{app}\AgeOfDuck.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\AgeOfDuck.exe"; Description: "Launch Age of Duck - AOE 2 Elo Overlay"; Flags: nowait postinstall skipifsilent

[Messages]
WelcomeLabel1=Welcome to the Age of Duck MOD Setup Wizard.
FinishedLabel=Thank you for installing Age of Duck Mod - The AoE 2 DE ELO & Helper by @BubbleDuck! Click Finish to exit.
