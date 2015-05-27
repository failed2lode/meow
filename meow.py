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
# walletPassxMaterialEncodedFilename = apg -a 1 -n 1 -m 16 -x 16 -M SNCL -c cl_seed -q # generates a 16 digit strong filename. check the -M setting to make sure the character set is appropriate
# qrencode -o walletPassxMaterialDirectory/walletPassxMaterialEncodedFilename walletPassxMaterial
#
#
# -- generate Ethereum wallet material
#   # use geth in non-interactive mode to create Ethereum wallet material
#   # see https://github.com/ethereum/go-ethereum/wiki/Managing-your-accounts
#
#  ethereumWalletAddress = geth --datadir WalletMaterialDirectory --password WalletPassxMaterialDirectory/WalletPassxMaterialFilename account new
#  # returns:   Address: b0047c606f3af7392e073ed13253f8f4710b08b6
#
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
#  # make it a QR code directly using qrencode http://packages.ubuntu.com/trusty/qrencode -> libqrencode from http://fukuchi.org/works/qrencode/index.html.en
#  # man page: http://manpages.ubuntu.com/manpages/trusty/man1/qrencode.1.html
#
# paperPassxMaterialEncodedFilename = apg -a 1 -n 1 -m 16 -x 16 -M SNCL -c cl_seed -q # generates a 16 digit strong filename. check the -M setting to make sure the character set is appropriate
# qrencode -o paperPassxMaterialDirectory/paperPassxMaterialEncodedFilename paperPassxMaterial
#
#  
# -- encrypt the ethereum wallet material
#
#
#
# -- QR encode the ethereum wallet material
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




          