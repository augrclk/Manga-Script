-- Manga Prompt Auto-Sender (JSON format)

set pyScript to POSIX path of (choose file with prompt "mouse_click.py dosyas›n› seç:")

set chosenFile to choose file with prompt "Prompt JSON dosyas›n› seç:" of type {"json", "public.plain-text"}
set fileContent to read chosenFile as «class utf8»

-- JSON'dan prompt de€erlerini çek
set promptTexts to {}
set AppleScript's text item delimiters to "\"Prompt_"
set chunks to text items of fileContent

repeat with i from 2 to count of chunks
	set chunk to item i of chunks
	-- Value k›sm›n› al (": " sonras›)
	set AppleScript's text item delimiters to "\": \""
	set parts to text items of chunk
	if (count of parts) > 1 then
		set valuePart to item 2 of parts
		-- Sonu bul (", sonraki key veya } öncesi)
		set AppleScript's text item delimiters to "\","
		set endParts to text items of valuePart
		set promptValue to item 1 of endParts
		-- Son } kontrolü
		set AppleScript's text item delimiters to "\"}"
		set endParts2 to text items of promptValue
		set promptValue to item 1 of endParts2
		-- Baﬂtaki ve sondaki t›rnaklar› temizle
		if promptValue starts with "\"" then
			set promptValue to text 2 thru -1 of promptValue
		end if
		if promptValue ends with "\"" then
			set promptValue to text 1 thru -2 of promptValue
		end if
		set end of promptTexts to promptValue
	end if
	set AppleScript's text item delimiters to "\"Prompt_"
end repeat

set AppleScript's text item delimiters to ""

set promptCount to (count of promptTexts) as string

display dialog promptCount & " prompt bulundu. Baﬂlayal›m m›?" buttons {"‹ptal", "Baﬂlat"} default button 2
if button returned of result is "‹ptal" then return

repeat with i from 10 to 1 by -1
	display notification "Baﬂl›yor: " & i & " saniye..." with title "Manga Sender"
	delay 1
end repeat

on pyClick(pyScript, x, y)
	do shell script "python3 " & quoted form of pyScript & " " & x & " " & y
	delay 1.5
end pyClick

repeat with i from 1 to count of promptTexts
	set thePrompt to item i of promptTexts
	set the clipboard to thePrompt
	
	pyClick(pyScript, 582, 1054)
	
	pyClick(pyScript, 710, 430)
	tell application "System Events"
		keystroke "3-Layout.jpeg"
		delay 1
		key code 36
	end tell
	delay 1.5
	
	pyClick(pyScript, 650, 1020)
	
	tell application "System Events"
		keystroke "v" using command down
		delay 1
		key code 36
	end tell
	
	delay 40
end repeat

display dialog "Tamamland›! " & promptCount & " prompt gönderildi." buttons {"Tamam"} default button 1