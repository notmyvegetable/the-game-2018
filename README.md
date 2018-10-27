# The Game - 2018 Edition 
Write-up for the beginner/intermediate CTF hosted in HackUPC.

### To do
Level 8

### Preface
In this write-up I will be explaining things and concepts as they were appearing back then in my mind, but I will not be showing any flags or spoonfeeding down to the littlest detail. You can follow along in [https://mail.biene.cat](https://mail.biene.cat).
This CTF had a healthy mix of everything as challenges, some harder than others, but with a nice lore behind everything. TheBlackJacks, a NSA hacker group, opened a position in their ranks, and after some trial to get in they make you conduct some criminal activities.
You engage with them using a mail webclient, located in https://mail.biene.cat

## 1st Level
[First mail](mail01)
First thing that crossed my mind was clicking that link and checking for hidden things inside of it. But after 20 minutes of nothing, I decided to check the mail again and realized that whatever is hidden could be inside the mail itself.

![img01](https://a.uguu.se/Rja4EflVbhws_chrome_2018-10-24_07-08-23.png)

And it was. After you send the password you receive the next mail.

## 2nd Level
[Second mail](mail02)
It's not hard to see that there are several letter in bold inside of the text, after separating them you get "laemdoog", reverse it and you get the password.

## 3rd Level
[Third mail](mail03)
This last step for their test might seem hard for those that don't see at first glance what those number mean. They are hexadecimal, so you just use a tool like [asciitohex](https://asciitohex.com) to convert it and after conversion it's just numbers all over again, but they are decimal, so you convert them from decimal and get the password.

(Before going to the next level I'd like to mention to one of the organizers whose name starts with B that remember only has one m, and I've seen that typo quite a few times already ;) )

## 4th Level
[Fourth mail](mail04)
You've been accepted into TheBlackJacks, now it's time for you to work for their clients.
In this mail they're asking you to hack into an administration panel and send them money from it and you get a webpage link.

First thing that crosses my mind to find an admin panel or similar is pulling out [gobuster](https://github.com/OJ/gobuster) or [dirbuster](https://www.owasp.org/index.php/Category:OWASP_DirBuster_Project), and so I did and found out the admin panel very easily. 
Reply with the admin panel URL to advance.

## 5th Level
[Fifth mail](mail05)
In the panel you see "Username", "Password" and "Weekly PIN" fields, and in the mail it says you need a secret PIN, first things I try anyway are SQLi and/or auth bypasses, but after testing for SQLi it seems like the input is ignored if you don't put a PIN, and basic SQLi doesn't work.

Next thing I did was check the cookies, and there was one called "logged" set to false. But after trying to set it to true and logging in with "admin:whatever" it doesn't seem to bypass the login. The thing you are asked for is the PIN, so let's find that first.

In the body you find a JS function defined called "weeklyPIN", which takes an seemingly numerical input and returns a number.
>function weeklyPIN(a) {
> return (((a >> 5)%18248502) << 3)*3;
>}

The most common way to represent time as a number is epoch, so they could've easily used that as an input. With online tools like [https://www.epochconverter.com/](https://www.epochconverter.com/) you can convert time to epoch, since it says in the website it is changed every monday at 3:00AM every week, you are supposed to use that time.

![time](https://a.uguu.se/c8VUK1u8GT47_chrome_2018-10-24_09-26-57.png)

Run that number as a parameter for the JS function found previously and that is the PIN!

## 6th Level
[Sixth mail](mail06)
Using the previously known knowledge of the cookie and now with the PIN we can start testing out more stuff.
Something I noticed previously is that you can do username enumeration. Putting an invalid username blurts out:
![invalid](https://a.uguu.se/YWtC2OSg4ILz_chrome_2018-10-24_09-42-19.png)
So we try until we find out one that works. Which "admin" is since we get this instead:
![invalidp](https://a.uguu.se/pklCcNAZc7qw_chrome_2018-10-24_09-43-56.png)

Now with a valid PIN and username we can try if the cookie auth bypass works by setting the cookie to true:
![cookie](https://a.uguu.se/oDeP0kHoRKiy_chrome_2018-10-24_09-45-27.png)

Which it indeed does, now when you're inside the panel you see some more information, and when you go into your profile tab you see in 2 fields that you cannot write into, but the "Password" field, contains something.
![passdw](https://a.uguu.se/Ghb2MhcXDvnf_chrome_2018-10-24_09-49-21.png)
The password (first few characters changed in the picture) is base64 encoded and all you need to do is decode it and send it in a mail.

## 7th Level
[Seventh mail](mail07)
After this level, things start getting slightly trickier. So you get a mail with an offer for a product that can make you stand strong against the challenges, both you and your little friend, if you have one.

They give you a map (maze.png in the repo), and you need to find the length of the path to the room, taking in account the costs of passing through a guard or a security camera.

This can be done using any algorithm to find a path, since after looking at the map for a bit you start noticing there are no loops (and you can check manually later with your algorithm anyway), and so you make a script to turn the map from a png into an array of values, and run the algorithm on that (you can check mine on the repo, "maze.py").

"For sure I know one thing, you prefer passing through a security camera rather than a guard!" means that you have to give the security camera a weight of 2 and the guard a 3, regular blocks are a 1, found this out by testing.

## 8th Level
[Eigth mail](mail08)
You get 2 mails again, one that provides a link to some tools [http://www.theblackjacks.tech](http://www.theblackjacks.tech), and the regular one.

You get a binary file attached in the mail (secdoor in the repo). The first thing that you do with binaries is opening them in [IDA](https://www.hex-rays.com/products/ida/) to get a grasp of what they do.
Opening it in IDA you find out that the main function only prints "BMP" and exits, which is suspicious, since this is the file with the key.
![BMP](https://a.uguu.se/MBEoaxxwsZTO_idaq64_2018-10-24_10-24-59.png)
If you check where that "BMP" string is located, you'll find there's 2 sectors of raw data that's never used inside of that file. First throught was to load the file inside of the tool they give you, and see what's in there. I first put all of those sectors inside their own files for ease of view, with a hex editor. 
They seemed like weird data so I carried on and saw there was trailing data at the end of the file..

## 9th Level
[Ninth mail](mail09)
Another binary, cool! (sec_door.bin in the repo) Same process, open up in IDA and check for functionality, in this case it seems like it's encoding your input and comparing with a predefined pin.
![main](https://a.uguu.se/sJF51RHwbrUH_idaq64_2018-10-26_12-18-23.png)
C equivalent.
![main_c](https://a.uguu.se/Atods8GirU2g_idaq64_2018-10-26_12-19-55.png)

Let's check what that encode function does... Turns out all it does is call the function "mystery" on some parts of the string.
![encode_c](https://a.uguu.se/iygY37rhBBwY_idaq64_2018-10-26_12-31-54.png)
And the mystery function just swaps the content of the pointers it is given, in this case, characters.
![mistery_c](https://a.uguu.se/2k4bHHLfZcVT_idaq64_2018-10-26_12-34-35.png)
So all you have to do to get the password, is reverse the pin in the way the "encode" function does. Easiest way to do that, run the binary on a debugger and let it do it for you, by passing it the pin and breaking on strcmp and checking the parameters.
![debug](https://a.uguu.se/dPzHaH6QDhNZ_idaq64_2018-10-26_12-46-58.png)
And that's the pin. (+4 to hide the first bytes of the flag)

## 10th Level
[Tenth mail](mail10)
You are given an image (credential.png on the repo), which is obviously a qr code, and when you decode it you get something resembling a RSA public key and some RSA encrypted data (creds.txt on the repo).
Seeing a RSA public key so tiny first thing that I thought of is to use an amazing tool for RSA key analysis in CTFs called [RsaCtfTool](https://github.com/Ganapati/RsaCtfTool), and running it on the key and the *base64 decoded* message, it gives you the flag.

## 11th Level
[Eleventh mail](mail11)
New mail... Ok let's check it... Huh a link... let's open it... What the flying fuck is this. Ok let's not get alarmed, might be weird, but it has to be solvable. By how it's displayed it's obvious that the image (example image otp.png in the repo) above contains a code that has to be decoded and put into the field in the webpage.
Inside the webpage you find a comment that's not left there for no reason:
><!-- Hilbert Inc. All rights reserved -->

Since the image seems to be encrypted or encoded in a search for "hilbert crypto" the term "hilbert curves" appears several times. Inside the wikipedia webpage for [Hilbert Curves](https://en.wikipedia.org/wiki/Hilbert_curve) you can see how they work.
Now that the algorithm is known, something that reverses it shouldn't be hard to do. After 4 hours of pain you notice it is and somehow you've failed to do a lot of stuff right and use part of the code that is on the wikipedia page as a base.
After you decode it you get a qr code, which you can decode on-site and display the OTP code to enter on the form. (My script is called hilbert.py on the repo, first argument is the name of the file and second is the number of iterations of the hilbert curve you want to apply)

## 12th Level
[Twelfth mail](mail12)
All that's well, ends well! But this wasn't well to begin with, so yeah.
This time you are given an image (hidden.png in the repo) with something hidden inside of it. After running several steganography tools and checking different automated techniques and getting nothing out of it (binwalk, reverse search for original and comparing, online steganography tools, steganabara, and many others) I decided to do it manually.
After splitting the image in red, green, and blue layers and checking each one of them, I noticed the blue channel had something resembling letters in the background. (hidden in blue in the mail was added afterwards as a clue)
![blue_channel](https://a.uguu.se/XGAvncB6Akqf_Photoshop_2018-10-27_07-51-57.png)
And so I decided to make a script to take the blue channel, accentuate it and separate it from the rest (hidden.py takes image as first argument and number for when to accentuate as second).
Some letters show up after you put 2 as the limit.
![]()
They seem to be reversed, and after reversing it, they seem to be passed through some ROT13 or similar, so after trying with different ROT values one of them gives in and the flag shows up.

## 13th Level
[Thirteenth mail](mail13)
The last frontier, one that you cannot cross unless you can traverse the boundaries of time and go back to HackUPC 2018 and beat me at The Game.

Not really, it wasn't anything godly, it was just going to the coordinates and getting the flag, but you're not going to get it unless you ask me in person, and I barely ever appear so good luck if you want it.

## You Win The Game
This edition of The Game was awesome, and the effort put in by the staff shows, I hope they are able to make next editions as great or even better!

Contact info: [Twitter](https://twitter.com/notmyvegetable)
Follow me for pictures of cats and other cute animals, you can also DM me for any details on the write-up.

[mail01]: 
[mail02]:
[mail03]: 
[mail04]:
[mail05]:
[mail06]: 
[mail07]: 
[mail08]: 
[mail09]:
[mail10]: 
[mail11]:
[mail12]:
[mail13]# The Game - 2018 Edition 
Write-up for the beginner/intermediate CTF hosted in HackUPC.

### To do
Level 8

### Preface
In this write-up I will be explaining things and concepts as they were appearing back then in my mind, but I will not be showing any flags or spoonfeeding down to the littlest detail. You can follow along in [https://mail.biene.cat](https://mail.biene.cat).
This CTF had a healthy mix of everything as challenges, some harder than others, but with a nice lore behind everything. TheBlackJacks, a NSA hacker group, opened a position in their ranks, and after some trial to get in they make you conduct some criminal activities.
You engage with them using a mail webclient, located in https://mail.biene.cat

## 1st Level
[First mail](mail01)
First thing that crossed my mind was clicking that link and checking for hidden things inside of it. But after 20 minutes of nothing, I decided to check the mail again and realized that whatever is hidden could be inside the mail itself.

![img01](https://a.uguu.se/Rja4EflVbhws_chrome_2018-10-24_07-08-23.png)

And it was. After you send the password you receive the next mail.

## 2nd Level
[Second mail](mail02)
It's not hard to see that there are several letter in bold inside of the text, after separating them you get "laemdoog", reverse it and you get the password.

## 3rd Level
[Third mail](mail03)
This last step for their test might seem hard for those that don't see at first glance what those number mean. They are hexadecimal, so you just use a tool like [asciitohex](https://asciitohex.com) to convert it and after conversion it's just numbers all over again, but they are decimal, so you convert them from decimal and get the password.

(Before going to the next level I'd like to mention to one of the organizers whose name starts with B that remember only has one m, and I've seen that typo quite a few times already ;) )

## 4th Level
[Fourth mail](mail04)
You've been accepted into TheBlackJacks, now it's time for you to work for their clients.
In this mail they're asking you to hack into an administration panel and send them money from it and you get a webpage link.

First thing that crosses my mind to find an admin panel or similar is pulling out [gobuster](https://github.com/OJ/gobuster) or [dirbuster](https://www.owasp.org/index.php/Category:OWASP_DirBuster_Project), and so I did and found out the admin panel very easily. 
Reply with the admin panel URL to advance.

## 5th Level
[Fifth mail](mail05)
In the panel you see "Username", "Password" and "Weekly PIN" fields, and in the mail it says you need a secret PIN, first things I try anyway are SQLi and/or auth bypasses, but after testing for SQLi it seems like the input is ignored if you don't put a PIN, and basic SQLi doesn't work.

Next thing I did was check the cookies, and there was one called "logged" set to false. But after trying to set it to true and logging in with "admin:whatever" it doesn't seem to bypass the login. The thing you are asked for is the PIN, so let's find that first.

In the body you find a JS function defined called "weeklyPIN", which takes an seemingly numerical input and returns a number.
>function weeklyPIN(a) {
> return (((a >> 5)%18248502) << 3)*3;
>}

The most common way to represent time as a number is epoch, so they could've easily used that as an input. With online tools like [https://www.epochconverter.com/](https://www.epochconverter.com/) you can convert time to epoch, since it says in the website it is changed every monday at 3:00AM every week, you are supposed to use that time.

![time](https://a.uguu.se/c8VUK1u8GT47_chrome_2018-10-24_09-26-57.png)

Run that number as a parameter for the JS function found previously and that is the PIN!

## 6th Level
[Sixth mail](mail06)
Using the previously known knowledge of the cookie and now with the PIN we can start testing out more stuff.
Something I noticed previously is that you can do username enumeration. Putting an invalid username blurts out:
![invalid](https://a.uguu.se/YWtC2OSg4ILz_chrome_2018-10-24_09-42-19.png)
So we try until we find out one that works. Which "admin" is since we get this instead:
![invalidp](https://a.uguu.se/pklCcNAZc7qw_chrome_2018-10-24_09-43-56.png)

Now with a valid PIN and username we can try if the cookie auth bypass works by setting the cookie to true:
![cookie](https://a.uguu.se/oDeP0kHoRKiy_chrome_2018-10-24_09-45-27.png)

Which it indeed does, now when you're inside the panel you see some more information, and when you go into your profile tab you see in 2 fields that you cannot write into, but the "Password" field, contains something.
![passdw](https://a.uguu.se/Ghb2MhcXDvnf_chrome_2018-10-24_09-49-21.png)
The password (first few characters changed in the picture) is base64 encoded and all you need to do is decode it and send it in a mail.

## 7th Level
[Seventh mail](mail07)
After this level, things start getting slightly trickier. So you get a mail with an offer for a product that can make you stand strong against the challenges, both you and your little friend, if you have one.

They give you a map (maze.png in the repo), and you need to find the length of the path to the room, taking in account the costs of passing through a guard or a security camera.

This can be done using any algorithm to find a path, since after looking at the map for a bit you start noticing there are no loops (and you can check manually later with your algorithm anyway), and so you make a script to turn the map from a png into an array of values, and run the algorithm on that (you can check mine on the repo, "maze.py").

"For sure I know one thing, you prefer passing through a security camera rather than a guard!" means that you have to give the security camera a weight of 2 and the guard a 3, regular blocks are a 1, found this out by testing.

## 8th Level
[Eigth mail](mail08)
You get 2 mails again, one that provides a link to some tools [http://www.theblackjacks.tech](http://www.theblackjacks.tech), and the regular one.

You get a binary file attached in the mail (secdoor in the repo). The first thing that you do with binaries is opening them in [IDA](https://www.hex-rays.com/products/ida/) to get a grasp of what they do.
Opening it in IDA you find out that the main function only prints "BMP" and exits, which is suspicious, since this is the file with the key.
![BMP](https://a.uguu.se/MBEoaxxwsZTO_idaq64_2018-10-24_10-24-59.png)
If you check where that "BMP" string is located, you'll find there's 2 sectors of raw data that's never used inside of that file. First throught was to load the file inside of the tool they give you, and see what's in there. I first put all of those sectors inside their own files for ease of view, with a hex editor. 
They seemed like weird data so I carried on and saw there was trailing data at the end of the file..

## 9th Level
[Ninth mail](mail09)
Another binary, cool! (sec_door.bin in the repo) Same process, open up in IDA and check for functionality, in this case it seems like it's encoding your input and comparing with a predefined pin.
![main](https://a.uguu.se/sJF51RHwbrUH_idaq64_2018-10-26_12-18-23.png)
C equivalent.
![main_c](https://a.uguu.se/Atods8GirU2g_idaq64_2018-10-26_12-19-55.png)

Let's check what that encode function does... Turns out all it does is call the function "mystery" on some parts of the string.
![encode_c](https://a.uguu.se/iygY37rhBBwY_idaq64_2018-10-26_12-31-54.png)
And the mystery function just swaps the content of the pointers it is given, in this case, characters.
![mistery_c](https://a.uguu.se/2k4bHHLfZcVT_idaq64_2018-10-26_12-34-35.png)
So all you have to do to get the password, is reverse the pin in the way the "encode" function does. Easiest way to do that, run the binary on a debugger and let it do it for you, by passing it the pin and breaking on strcmp and checking the parameters.
![debug](https://a.uguu.se/dPzHaH6QDhNZ_idaq64_2018-10-26_12-46-58.png)
And that's the pin. (+4 to hide the first bytes of the flag)

## 10th Level
[Tenth mail](mail10)
You are given an image (credential.png on the repo), which is obviously a qr code, and when you decode it you get something resembling a RSA public key and some RSA encrypted data (creds.txt on the repo).
Seeing a RSA public key so tiny first thing that I thought of is to use an amazing tool for RSA key analysis in CTFs called [RsaCtfTool](https://github.com/Ganapati/RsaCtfTool), and running it on the key and the *base64 decoded* message, it gives you the flag.

## 11th Level
[Eleventh mail](mail11)
New mail... Ok let's check it... Huh a link... let's open it... What the flying fuck is this. Ok let's not get alarmed, might be weird, but it has to be solvable. By how it's displayed it's obvious that the image (example image otp.png in the repo) above contains a code that has to be decoded and put into the field in the webpage.
Inside the webpage you find a comment that's not left there for no reason:
><!-- Hilbert Inc. All rights reserved -->

Since the image seems to be encrypted or encoded in a search for "hilbert crypto" the term "hilbert curves" appears several times. Inside the wikipedia webpage for [Hilbert Curves](https://en.wikipedia.org/wiki/Hilbert_curve) you can see how they work.
Now that the algorithm is known, something that reverses it shouldn't be hard to do. After 4 hours of pain you notice it is and somehow you've failed to do a lot of stuff right and use part of the code that is on the wikipedia page as a base.
After you decode it you get a qr code, which you can decode on-site and display the OTP code to enter on the form. (My script is called hilbert.py on the repo, first argument is the name of the file and second is the number of iterations of the hilbert curve you want to apply)

## 12th Level
[Twelfth mail](mail12)
All that's well, ends well! But this wasn't well to begin with, so yeah.
This time you are given an image (hidden.png in the repo) with something hidden inside of it. After running several steganography tools and checking different automated techniques and getting nothing out of it (binwalk, reverse search for original and comparing, online steganography tools, steganabara, and many others) I decided to do it manually.
After splitting the image in red, green, and blue layers and checking each one of them, I noticed the blue channel had something resembling letters in the background. (hidden in blue in the mail was added afterwards as a clue)
![blue_channel](https://a.uguu.se/XGAvncB6Akqf_Photoshop_2018-10-27_07-51-57.png)
And so I decided to make a script to take the blue channel, accentuate it and separate it from the rest (hidden.py takes image as first argument and number for when to accentuate as second).
Some letters show up after you put 2 as the limit.
![]()
They seem to be reversed, and after reversing it, they seem to be passed through some ROT13 or similar, so after trying with different ROT values one of them gives in and the flag shows up.

## 13th Level
[Thirteenth mail](mail13)
The last frontier, one that you cannot cross unless you can traverse the boundaries of time and go back to HackUPC 2018 and beat me at The Game.

Not really, it wasn't anything godly, it was just going to the coordinates and getting the flag, but you're not going to get it unless you ask me in person, and I barely ever appear so good luck if you want it.

## You Win The Game
This edition of The Game was awesome, and the effort put in by the staff shows, I hope they are able to make next editions as great or even better!

Contact info: [Twitter](https://twitter.com/notmyvegetable)
Follow me for pictures of cats and other cute animals, you can also DM me for any details on the write-up.

[mail01]: 
[mail02]:
[mail03]: 
[mail04]:
[mail05]:
[mail06]: 
[mail07]: 
[mail08]: 
[mail09]:
[mail10]: 
[mail11]:
[mail12]:
[mail13]::
