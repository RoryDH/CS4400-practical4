# Password cracking on AWS Assignment

- Add the https://pushmore.io/ telegram bot
- Copy the token at the end of your pushmore URL and paste it in a file named `push_more_token.txt`
- Make a file named by the [hashcat algorithm number](https://hashcat.net/wiki/doku.php?id=hashcat) with the extension `.hashes`. For example for descrypt, name it `1500.hashes`
- Ensure all the algo numbers you want to run are in the `ALGO_NUMS` array at the top of `main.py`
- `ln -s $(which hashcat) hashcat`
- Find a copy of rockyou.txt on le web.
- `python3 main.py`
