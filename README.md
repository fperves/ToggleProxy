ToggleProxy
===========

Purpose
-------
ToggleProxy is an utility that eases the activation / deactivation of proxy configuration in Windows 7, by providing a tray icon that proposes the options to :
  * deactivate proxy (removes auto-configuration URL of proxy config, and disable the proxy config),
  * activate proxy (restores auto-configuration URL and re-activates proxy),
  * open windows proxy configuration page.

Requirements
------------
The tray is built from to infi.systray library.

to install the required library, simply run the following command : 
  
    pip install -r requirements.txt 

Credits
-------
infi.systray : https://github.com/Infinidat/infi.systray
