Starting
	double click RUNME.ps1 and "Run with Powershell"

Stopping
	ctrl+C
	wait for mosquitto to terminate
	close the powershell window


Please do not edit "originals" folder. Using that as a fallback / save point.


manual options, see "wsl_script" file.

Open WSL Ubuntu-20.04 (orange icon on taskbar):

1. "mosquitto"
		starts the Mosquitto MQTT broker
2. wait few sec for the broker to spin up
3. "python3 /mnt/c/python_code/Qualisys_MQTT/mqtt_Qualisys_pub.py"
		starts the universal publisher (please do not edit)
4. "python3 /mnt/c/python_code/capstones/bridge/sub_log.py"
		starts the subscription for your application (feel free to edit as you like)

general, "&" at the end of a line makes that process run in the background.





regedit notes to make ps1 executable:
https://stackoverflow.com/questions/10137146/is-there-a-way-to-make-a-powershell-script-work-by-double-clicking-a-ps1-file

HKEY_CLASSES_ROOT\Microsoft.PowerShellScript.1\Shell\open\command

"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe" -noLogo -ExecutionPolicy unrestricted -file "%1"
