@echo off
rem Double-click in the folder containing the .part files. Creates GTA6_might_be_worse_v3.mp4
copy /b GTA6_might_be_worse_v3.mp4.00.part + GTA6_might_be_worse_v3.mp4.01.part GTA6_might_be_worse_v3.mp4
certutil -hashfile GTA6_might_be_worse_v3.mp4 SHA256
echo Expected: 24f482a28b8db5a1de4f811422aaccd6c328c3cedbce1ef2cec36c9f5cc415ec
pause
