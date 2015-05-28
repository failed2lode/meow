#!/usr/bin/python

# this is the main script for 'my Ethereum offline wallet' or meow.
# code 2015 by failed2lode@gmail.com and hopefully others.
# see https://github.com/failed2lode/meow for readme and other information
# started May 2015

# this is pre-alpha code and at this stage we're just scaffolding out the functionality.

# proposed usage
#
# meow 
#      generate        
#                 -testprint # print test page ( on | off )
#      
#       decode
#                 - directory # use the specified directory as a target directory ( what is the default?)        
#                 

# proposed workflow
#
# meow generate 
#
# splash
# 
# -- print test page --
# if print test page
# 		splash "print test page now?" (yes | don't bother | quit)
#		Print test page
# 		splash "was test print successful?" (yes | retry | quit)
#
# -- create temp directories --
# the idea here is to use random sort of hidden '.' directories and never place materials together in a single directory. No idea how effective this will be.
# as a random thought, is there a way to create a temp ram disk to stick this in to promote absolute destruction when we don't need it anymore?
#
#		walletPassxMaterialDirectory = mkdir /tmp + /. + apg -a 1 -n 1 -m 16 -x 16 -M SNCL -c cl_seed -q # generates a 16 digit strong filename. check the -M setting to make sure the character set is appropriate
#		walletMaterialDirectory      = mkdir /tmp + /. + apg -a 1 -n 1 -m 16 -x 16 -M SNCL -c cl_seed -q # generates a 16 digit strong filename. check the -M setting to make sure the character set is appropriate
#		paperPassxMaterialDirectory  = mkdir /tmp + /. + apg -a 1 -n 1 -m 16 -x 16 -M SNCL -c cl_seed -q # generates a 16 digit strong filename. check the -M setting to make sure the character set is appropriate
# 
# # for each of these directories we may need to chmod it to lock it down permission wise. check when writing.
# 		
# -- generate Ethereum wallet passx material
# 	# use apg to generate strong password material. see http://linux.die.net/man/1/apg for man page. 
#   # walletPassx needs to be saved to a file for use by geth in non-interactive mode. This sucks.
#   # do not make it worse by naming it something obvious
# walletPassxMaterialFilename = apg -a 1 -n 1 -m 16 -x 16 -M SNCL -c cl_seed -q # generates a 16 digit strong filename. check the -M setting to make sure the character set is appropriate
# apg -a 1 -n 1 -m 16 -x 16 -M SNCL -c cl_seed -q > walletPassxMaterialDirectory/walletPassxMaterialFilename # generates a 16 digit strong password. Comments welcome on these settings.
#
# -- QRencode wallet passx material  
#  # since we are here, generate the QR encoded version of this passphrase at the same time
#  # make it a QR code directly using qrencode http://packages.ubuntu.com/trusty/qrencode -> libqrencode from http://fukuchi.org/works/qrencode/index.html.en
#  # man page: http://manpages.ubuntu.com/manpages/trusty/man1/qrencode.1.html
#
#  walletPassxMaterial = file.read(walletPassxMaterialDirectory/walletPassxMaterialFilename)
#  qrencode -o walletPassxMaterialDirectory/walletPassxMaterialEncodedFilename walletPassxMaterial
# 
#
# -- generate Ethereum wallet material
#   # in this v1 we use geth in non-interactive mode to create Ethereum wallet material
#   # see https://github.com/ethereum/go-ethereum/wiki/Managing-your-accounts
#
#  ethereumWalletAddress = geth --datadir WalletMaterialDirectory --password WalletPassxMaterialDirectory/WalletPassxMaterialFilename account new
#  # returns:   Address: b0047c606f3af7392e073ed13253f8f4710b08b6
#
#  # note this is very insecure as it requires use of a plaintext password file and returns a plaintext wallet file.
#  # in next version remove this and move to in-memory wallet gen using python code from pythereum or similiar 
#  # not doing in this version as I do not understand that code and want to get an MVP knocked out for demo purposes
#
#
# -- remove persistent items from disk
#  # the Ethereum wallet and the wallet passx material are at this moment in plaintext on the disk
#  # load them into memory immediately and securely delete them from the disk
#
# walletPassxMaterialEncoded = file.read(walletPassxMaterialDirectory/walletPassxMaterialEncodedFilename)
# srm -r walletPassxMaterialDirectory
#
# walletMaterial = file.read(walletMaterialDirectory/whateverthe walletnameconstructis
# srm -r walletMaterialDirectory
#
#  # note there are lots of issues with srm, wipe, etc, in journalled file sywtems and ssd volumes. so this is not a solution, it is an attempt to mitigate which may be very ineffective.
#
# -- generate paperPassx material
# 	# use apg to generate strong password material. see http://linux.die.net/man/1/apg for man page. 
#   # paperPassx material does not need to be saved to a file.
#   # but we do need to save a QR encoded copy of it for printing, so its almost the same thing. still sucks.
#   # do not make it worse by naming it something obvious
# paperPassxMaterial= apg -a 1 -n 1 -m 16 -x 16 -M SNCL -c cl_seed -q # generates a 16 digit strong passcode. 
#  
#
# -- QRencode paperPassx material
#  # order of operations is important here: you must delete the qr codes as you go to ensure they qre not ever all on the disk at the same time.
#  # make it a QR code directly using qrencode http://packages.ubuntu.com/trusty/qrencode -> libqrencode from http://fukuchi.org/works/qrencode/index.html.en
#  # man page: http://manpages.ubuntu.com/manpages/trusty/man1/qrencode.1.html
#
# paperPassxMaterialEncodedFilename = apg -a 1 -n 1 -m 16 -x 16 -M SNCL -c cl_seed -q # generates a 16 digit strong filename. check the -M setting to make sure the character set is appropriate
# qrencode -o paperPassxMaterialDirectory/paperPassxMaterialEncodedFilename paperPassxMaterial
#
#  # now immediately read the qr encoded material into memory and delete it from the disk. 
# paperPassxMaterialEncoded = file.read(paperPassxMaterialDirectory/paperPassxMaterialEncodedFilename)
# srm -r paperPassxMaterialDirectory
#
#
# -- encrypt the ethereum wallet material
#   # assuming we are using some sort of python openssl implementation so not too concerned about getting command line arguments here right
# walletMaterialEncrypted = openssl(walletMaterial, paperPassxMaterial)
# 
#  # It's not clear to me if we need to uuencode/xxd the output of the encryption step if we are storing it in a QRcode.
#  # for sake of following  a known good tutorial, I am going to include it
#  # if it turns out to be unnecessary, this is an invitation to pull request it out.
#  # again, assuming there is some pythoin implementation so not too worried yet about syntax
# walletMaterialEncryptedUuencoded = uuencode(walletMaterialEncrypted)
#
#
# -- QR encode the encrypted encoded wallet material
#
#
#
#
#
#
#
#
#
#
# -- Securely delete anything that is not a QR encoded material
# 
#
# -- lay out page 1: encrypted encoded ethereum wallet material printout
#
# -- lay out page 2: encoded wallet passx and encoded paper passx
#
# -- securely delete everything you have not deleted yet
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#




          