# meow
My Ethereum Offline Wallet (meow) script

## Background

Ethereum is a blockchain-based distributed consensus technology similiar to Bitcoin.
Use of Ethereum requires the establishment of a digital 'wallet' which contains cryptographic materials.
The cryptographic materials may be used to access value encoded in the blockchain.

A key risk of using Ethereum, Bitcoin, or any other blockchain-based technology is the loss of the wallet-based cryptographic materials.
This may occur through misfortune or the misdeeds of others.
Best practice in mitigating this risk is to store the cryptographic materials 'offline'  by literally printing them on paper and then destroying any online copies so they may not be accessed using digital means.

The Ethereum project is approaching a public launch and focussed on technologies core to the global release.
A script or method for easily creating offline wallets has not been provided by the core team.
This project attempts to provide a script for rudimentary functionality that may be built upon to securely and easily generate the required cryptographic materials and store them offline.

Having no expertise in Ethereum, this is being used as a learning opportunity.
The code is provided without warranty or guarantee. 
Use at your own risk.
Please contribute via pull requests, or fork for customization.

## Background Materials
These are the materials I assembled as background reading, in attempting to understand how to automate the process of creating offline Ethereum materials.

#### https://github.com/ethereum/go-ethereum/wiki/Mining

In order to earn ether through you need to have a coinbase (or etherbase) address set. This etherbase defaults to your primary account. If you got no etherbase address set, then geth --mine will not start up.

		> eth.coinbase
		'0x'
		> admin.newAccount()
		The new account will be encrypted with a passphrase.
		Please enter a passphrase now.
		Passphrase:
		Repeat Passphrase:
		'ffd25e388bf07765e6d7a00d6ae83fa750460c7e'
		> eth.coinbase
		'0xffd25e388bf07765e6d7a00d6ae83fa750460c7e'

#### https://github.com/ethereum/go-ethereum/wiki/Managing-your-accounts

Interactive use

		$ geth -datadir /tmp/eth  account new
		The new account will be encrypted with a passphrase.
		Please enter a passphrase now.
		Passphrase:
		Repeat Passphrase:
		Address: {7f444580bfef4b9bc7e14eb7fb2a029336b07c9d}
		
		$ geth --datadir /tmp/eth  account list
		Address: {7f444580bfef4b9bc7e14eb7fb2a029336b07c9d}
		
		$ geth --datadir /tmp/eth.0  account import ./key.prv
		The new account will be encrypted with a passphrase.
		Please enter a passphrase now.
		Passphrase:
		Repeat Passphrase:
		Address: {7f444580bfef4b9bc7e14eb7fb2a029336b07c9d}
Non-interactive use

You supply a plaintext password file as argument to the --password flag.

Note: Supplying the password directly as part of the command line is not encouraged, but you can always use shell trickery to get round this restriction.

		$ geth --datadir /tmp/eth --password /path/to/password account new
		Address: b0047c606f3af7392e073ed13253f8f4710b08b6
		
		$ geth --datadir /tmp/eth account list
		Address: {b0047c606f3af7392e073ed13253f8f4710b08b6}
		
		$ geth --datadir /tmp/eth1 --password /path/to/anotherpassword account import ./key.prv
		Address: b0047c606f3af7392e073ed13253f8f4710b08b6

#### https://medium.com/@abrkn/obtaining-and-offline-securing-ether-for-the-upcoming-ethereum-launch-157963b6a456
(note that I am paraphrasing this post and moving steps around to suit my partiocular need. To understand the material completely you should read the raw post in it's entirety several times)

Encrypt the ether.json file with DES3 and store it in ether.json.des3:

		$ cat ether.json | openssl des3 > ether.json.des3
		enter des-ede3-cbc encryption password:
		Verifying — enter des-ede3-cbc encryption password:
		

The file is now in binary and cannot easily be displayed in our terminal or printed on paper. The square looking characters are the ones that have no visual representation.

This makes printing the encrypted wallet a problem.

Luckily, there are tools to convert binary data to more readable formats. We'll use a tool called xxd which limits the character set to 0-9 and a-f:

		$ cat ether.json.des3 | xxd -p -c40 > ether.json.des3.xxd

to use a QRCode:

Open up the file, ether.json.des3.b4, in a text editor

Head over to http://goqr.me/ which has an easy to use QR Code generator. (must be a better way)


Now, the most important step. Print on a physical printer.

To restore:
 - if you have a QR code, read the code and save the result into a file called restore.txt
 - if you do not have a QR code, sucks to be you, you need to type the printed material into a file called ‘restore.txt’ 

		$ cat restore.txt | xxd -p -r | openssl des3 -d

At this point you should have the restored file.

####http://forum.ethereum.org/discussion/2114/where-are-my-config-files-go-and-cpp/p1

#####Ubuntu
The below relates to installs compiled from source.

		=== C++ ===
		AlethZero
		~/.ethereum/ (contains the blockchain state)
		~/.web3 (contains your keys)
		~/.config/ethereum/alethzero.conf (contains AZ preferences)

Eth

		~/.ethereum/ (contains the blockchain state and keys, shares them with alethzero)
		~/.web3 (contains your keys, shares them with alethzero)

For both Eth and AlethZero, the DAG is stored in ~/.ethash


		=== Go ===

		Geth:
		~/.ethereum (contains the chain, as well as your keys are in the /keystore subfolder)
		~/.ethash (contains the DAG when mining)

I will not list Mist settings here as it's under alpha development and rapidly changing. Your mileage may vary.

#####Conflicts!
The bad news is, on Ubuntu, both the Go and the C++ client share the same folder for blockchain storage. This means if you'd like to run both on the same machine, you'll have to use either the --datadir argument for Geth or the --db-path on Eth. Mist and Alethzero are however as far as I know not configurable at boot and will therefore lead to clashes, to run both of these the use of VMs is recommended until this is resolved.