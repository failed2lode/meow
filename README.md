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

### Warning
Having no expertise in Ethereum, this is being used as a learning opportunity.
The code is provided without warranty or guarantee. 
Use at your own risk.
Please contribute via pull requests, or fork for customization.

### Assumptions
I am using Ubuntu as an OS for my Ethereum activities.
Ubuntu 14.04 is supported for Ethereum.
This script is therefore, for now, Ubuntu 14.04 specific.
 

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

##### === C++ ===
		AlethZero
		~/.ethereum/ (contains the blockchain state)
		~/.web3 (contains your keys)
		~/.config/ethereum/alethzero.conf (contains AZ preferences)

##### Eth

		~/.ethereum/ (contains the blockchain state and keys, shares them with alethzero)
		~/.web3 (contains your keys, shares them with alethzero)

For both Eth and AlethZero, the DAG is stored in ~/.ethash


##### === Go ===

##### Geth:
		~/.ethereum (contains the chain, as well as your keys are in the /keystore subfolder)
		~/.ethash (contains the DAG when mining)

I will not list Mist settings here as it's under alpha development and rapidly changing. Your mileage may vary.

#####Conflicts!
The bad news is, on Ubuntu, both the Go and the C++ client share the same folder for blockchain storage. This means if you'd like to run both on the same machine, you'll have to use either the --datadir argument for Geth or the --db-path on Eth. Mist and Alethzero are however as far as I know not configurable at boot and will therefore lead to clashes, to run both of these the use of VMs is recommended until this is resolved.

## Usability

There are numerous usability hurdles that must be overcome. 
These span from very important to very trivial.
This section is not exhaustive, but does contain an overview of the issues I am most interested in addressing.

### Materials Handled and Stored Offline

In the non-interactive use case listed above:

		$ geth --datadir /tmp/eth --password /path/to/password account new
		Address: b0047c606f3af7392e073ed13253f8f4710b08b6

shown in pseudo-math:

		raw material + passphrase = Ethereum wallet file		

where it is made known elsewhere that all Ethereum wallet files require a passphrase to be usable.

Similarly, where

		$ cat ether.json | openssl des3 > ether.json.des3
		enter des-ede3-cbc encryption password:
		Verifying — enter des-ede3-cbc encryption password:		

then		

		Ethereum wallet file + des-ede3-cbc encryption password = encrypted Ethereum wallet file

which when encoded into a QR code:

		encrypted Ethereum Wallet file + QR encoder = QR-encoded encrypted Ethereum wallet file

may be securely printed and later retreived for use with a 'relatively' minimal effort.

In the tutorial at https://medium.com/@abrkn/obtaining-and-offline-securing-ether-for-the-upcoming-ethereum-launch-157963b6a456 referenced above,
you will note that the author refers to the passwords referenced above as:

 - the 'wallet' password or passphrase
 - the 'paper' password or passphrase
 
The tutorial author mentions:

 		I actually included my wallet password (not paper password) on the print outs as I do not consider them to be sensitive. 
 
For the paper password, it can be seen in one of the graphics that he has written on the printout of the encrypted wallet file "Klaus has the password".
This is a strategy of keeping the password redundantly secret by ensuring that a second person also has teh secret in case the first person forgets it or is somehow lost to the recovery process.
 
For an intentional and thoughtful user of Ethereum, this may be functional, but for a casual user, this is insufficient care of the password/passphrase materials, which must also be retained for the Ethereum wallet to be later recoverable from offline storage for subsequent use.
In fact, the materials which must be stored in some format on paper include:

 - the Ethereum wallet file
 - the 'wallet' password or passphrase
 - the 'paper' password or passphrase

To care properly for the password/passphrase (from here on referred to as the 'passx') materials, the following best practices may apply:
 - generate the passx materials using a generator designed for the task
 - encode the passx material as a QR code
 - print the encoded passx materials on a separate sheet of paper so it may be separately stored.
 
Note the storage of the passx materials on paper in unencrypted format will make some people uneasy. 
This is a valid concern, as unencrypted materials are intrinsically vulnerable.
However, from a usability perspective there is little choice:
 - the passx material needs to be stored somewhere
 - most casual users do not have password managers
 - passsword manager usage is usually inconsistent and has a high churn rate even among concerned users
 - encrypting the passx materials would reguire generation of an additional set of passx materials which would then require storage
 - etc.
 
In short, there is no good solution to the passx storage problem.
Rather than gloss over it ("Klaus has a copy") this is an intentioamnl strategy to balance usability with obfuscation:
 - the QR encoded masterials cannot be casually decoded
 - no unencoded versions are displayed or provided
 - QR decoders are required for the other materials, so they are in theory usable here
 
Each of the passx materials may be printed and stored separately, or they could be printed on a common sheet of paper, as without the Ethereum wallet material they are without use even if discovered together.     		
This is true even if the Ethereum address is known, as the address + passx of the Ethereum wallet together are not enough to reconstruct the Ethereum wallet material.

This method produces two printouts:
 - the encoded encrypted Ethereum wallet printout
 - the encoded (but not encrypted) passx printout
  
In order to match these at a later date, each printout should include the Ethereum address to which they pertain.
This address may also be QR encoded and / or barcoded for easy retreival.
It is expected that after all of this, a casual user will staple the sheets together and throw them in a desk drawer. 
A more appropriate or 'enterprise' storage strategy will involve separated storage of copies of the printouts in diverse locations. 

### Attack Vectors

The best scenario for running a tool like this would be to install it on a copy of Tails, which would destroy all evidence of its operation when complete through the Amnesic characteristics of it's operation.
At this time the Ethereum software will not install or operate on Tails, so we must intentionally replicate the destruction of all records of operation:

 - where possible, all temp files should be constrained to a single directory. It may be useful to set this disk up as a ram disk to facilitate subsequent secure removal.
 - where temp files cannot be constrained to the target temp directly, they will need to be explicltly identified
 - materials should never be displayed on the monitor
 - passx materials should not be requested from users
 - a scrambled full page footer should be printed after the printing is complete, to 'reset' the printer in case the image may be retained on the print head.				
 - where possible, printing should be limited to directly connected printers to avoid the possibility of copies of the materials being stored in a print queue or being retained in some other way 
 - directly after use or as quickly as possible during the execution of the script, all temp directories and files should be securely destroyed using a tool designed for the purpose which will overwrite the disk locations multiple times using random patterns. It is important to do this 'as you go' so you may ensure the materials are not stranded by a crash, or a user who shuts down the computer before the secure wiping is completed (it can take some time).
 - after use, the memory should be similiarly securely wiped. This probably requires a shutdown to accomplish.
 
### Printer Issues 

The possibility of the printer working flawlessly every time at the end of the script execution is zero.
To avoid the case where the script executes and then the printer does not work, it is advisable to default to a test print up front.
This will force the identification of printer issues prior to any material generation.
This test print should be switchable (on|off) on the command line where the printer is known to work, or where multiple wallets are being processed in a row.   
 
An alternative scenario is to require a test print, and use the test print to print the 'back' of the offline wallet.
This would require the user to retreive the paper from the printer once printed, turn it over, and reload it so the other side may be used for materials.
The nominal benefit is to print over the areas which would otherwise be susceptable to surreptitious viewing from the reverse side. 
However, this benefit must be weighed against the possibility of the user incorrectly loading the test print back into the printer correctly, if they bother to do it at all.

