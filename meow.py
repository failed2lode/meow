#!/usr/bin/env python

# this is the main script for 'my Ethereum offline wallet' or meow.
# code 2015 by failed2lode@gmail.com and hopefully others.
# see https://github.com/failed2lode/meow for readme and other information
# started May 2015

# this is pre-alpha code and at this stage we're just scaffolding out the functionality.

# proposed usage
#
# meow 
#      generate        
#      
#       decode
#                 - directory # use the specified directory as a target directory ( what is the default?)        
#                 

from optparse import OptionParser
import os
import sys

#-- Set Up page layout stuff
#  # using python image library. see http://effbot.org/imagingbook/image.htm and various other pages at the url.
from PIL import Image # do this once
from PIL import ImageFont # do this once
from PIL import ImageDraw # do this once
import StringIO
import subprocess  



def main_options():
    """Handles command-line interface, arguments & options. """

    usage = 'Usage: %prog {generate|decode} [OPTIONS]'
    parser = OptionParser(usage)
    parser.add_option('-w','--wallet', dest='wallet_dir', metavar='./WALLET',
            default='./purrrse',
            help='path to wallet dir; default is %default')

    (options, args) = parser.parse_args()

    if not len(args) == 1:
        parser.error('Incorrect number of arguments; see --help.')
    if args[0] not in ['generate','decode']:
        parser.error('Incorrect action specified; use generate or decode.')

    return (options, args)


def splash(message):
    """Clear the screen and display information."""

    try:
        os.system('clear')
        print( '  \n    \n')
        print( ' /\_/\    ')
        print( "(='.'=)   "+ message)
        print( ' > ^ <    ')
        print(  '\n\n'     )
    except Exception as e:
        print('Error displaying message: ' + str(e))


def print_test_page():
    """Print a test page."""
    
    #  Confirm Test Print Desired
    print_test_page_menu = "placeholder"
    
    while not print_test_page_menu.lower()[0] in ("y", "q", "n"):
        print_test_page_menu = raw_input('Print test page now? (Yes | No | Quit): ')

    if print_test_page_menu.lower()[0] == 'q':
        splash('goodbye!')
        raise Exception('Program cancelled by User')
    elif print_test_page_menu.lower()[0] == 'n':
        return
    
    #generate test page    
    print_font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSerif.ttf", 16) #may want to play with this; very ubuntu specific.  
    
    test_page = Image.new("RGB", (850, 1100), 'white')  # assuming an 8.5 x 11 page at 300 DPI, no margin, fully specified
    test_page_message = "This test page is being printed to ensure your printer is working purrfectly."
               
    #    lay out the page   
    draw = ImageDraw.Draw(test_page)
    draw.text((10, 110), ' /\_/\  ',(0,0,0),font=print_font)
    draw.text((10, 124), "(='.'=) meow test page",(0,0,0),font=print_font)
    draw.text((10, 138), ' > ^ <  ',(0,0,0),font=print_font)
    draw.text((10, 144), test_page_message ,(0,0,0),font=print_font)
    draw = ImageDraw.Draw(test_page)
    
    test_page.save('test_page.jpg', 'JPEG')
    test_page.save('test_page.png', 'PNG')
    test_page.save('test_page.bmp', 'BMP')
        
    test_print_success = "placeholder"
    while not test_print_success.lower()[0] in ('y', 'r', 'q'):

        try:
    
            # generate the page
            lpr =  subprocess.Popen("/usr/bin/lpr", stdin=subprocess.PIPE)
            output = StringIO.StringIO()
            format = 'PNG' # or 'JPEG' or whatever you want
            
            test_page.save(output, format)
            lpr.communicate(output.getvalue())
                        
            output.close()
            lpr.terminate()
            
            test_print_success = raw_input( 'Was test print successful? (Yes | Retry | Quit)')
            if test_print_success.lower()[0] == 'q':
                splash('goodbye!')
                raise Exception('Program cancelled by User')
            elif test_print_success.lower()[0] == 'y':
                return
            elif test_print_success.lower()[0] == 'r':
                test_print_success = "placeholder"
                    
        except Exception as e:
            print('Error attempting to print:' + str(e)) 
            pass
    
if __name__ == '__main__':

    (options, args) = main_options()

    if args[0] == 'decode':
        sys.exit(0)

    try:
        splash(u"meow")
        print_test_page()
        # create_memoryfs() - if we must store files, use a RAM drive.
        # generate_wallet() - is your goal to also generate the wallet in json?
        # encrypt (article mentions 3DES, but AES may be a more modern choice).
        # encode() to printable characters if not part of encrypt().
        sys.exit(0)
    except Exception as e:
        print('Error in __main__():' + str(e))
        pass
    finally:
        # Destroy all work material unconditionally.
        pass

############################################################################################
# proposed workflow
#
# meow generate 
#
# -- splash
#
#  # may want to put a message box up at some point with a graphic and a rolling message log so users can see that something is happening
#
#
#
#
# -- Set Up page layout stuff
#  # using python image library. see http://effbot.org/imagingbook/image.htm and various other pages at the url.
#  # this is abbreviated pseudo-code but you get the idea
#
# from PIL import Image # do this once
# from PIL import ImageFont # do this once
# from PIL import ImageDraw # do this once
# font = ImageFont.truetype("sans-serif.ttf", 16)
#
#
# -- print test page --
#
#  splash "print test page now?" (yes | don't bother | quit)
#  if print test page
#   test_page = Image.new("RGB", (2550, 3300), "white")  # assuming an 8.5 x 11 page at 300 DPI, no margin, fully specified
#       #  we could also use a meow background image of some kind ??
#
#    #lay out the page
# 
#    # it would be fun to put a meow header image here... 
#
#    test_page.draw.text((x, y),"This test page is being printed to ensure your printer is working.",(255,255,255),font=font) # I can imagine the instructions for this need to be wordsmithed a bit?
#    test_page.paste(walletPassxMaterialEncodedPIL, (x,y))
#
#    # maybe a meow footer of some kind too
#  
#    # print it
#      do while testPrintSuccess = retry {
#            test_page.save("/dev/lpr")
#
# 	         splash "was test print successful?" (testPrintSuccess= yes | retry | quit)
#
#       }
#
# -- create temp directories --
# the idea here is to use random sort of hidden '.' directories and never place materials together in a single directory. No idea how effective this will be.
# as a random thought, is there a way to create a temp ram disk to stick this in to promote absolute destruction when we don't need it anymore?
# it would also be good to encrypt anything held to disk. how to implement that?
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
#  # use this to generate an address string for pater printing
# wallet_address_string = "the address of this Ethereum Offline wallet is " + ethereumWalletAddress

#  # note this is very insecure as it requires use of a plaintext password file and returns a plaintext wallet file.
#  # in next version remove this and move to in-memory wallet gen using python code from pythereum or similiar 
#  # not doing in this version as I do not understand that code and want to get an MVP knocked out for demo purposes
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
#  # order of operations is important here: you must delete the qr codes as you go to ensure they qre not ever all on the disk at the same time.
#  # make it a QR code directly using qrencode http://packages.ubuntu.com/trusty/qrencode -> libqrencode from http://fukuchi.org/works/qrencode/index.html.en
#  # man page: http://manpages.ubuntu.com/manpages/trusty/man1/qrencode.1.html
#
# paperPassxMaterialEncodedFilename = apg -a 1 -n 1 -m 16 -x 16 -M SNCL -c cl_seed -q # generates a 16 digit strong filename. check the -M setting to make sure the character set is appropriate
# qrencode -o paperPassxMaterialDirectory/paperPassxMaterialEncodedFilename paperPassxMaterial
#
#
# -- encrypt the ethereum wallet material
#   # assuming we are using some sort of python openssl implementation so not too concerned about getting command line arguments here right
# walletMaterialEncrypted = openssl(walletMaterial, paperPassxMaterial)
# 
#  # It's not clear to me if we need to uuencode/xxd the output of the encryption step if we are storing it in a QRcode.
#  # for sake of following  a known good tutorial, I am going to include it
#  # if it turns out to be unnecessary, this is an invitation to pull request it out.
#  # again, assuming there is some python implementation so not too worried yet about syntax
# walletMaterialEncryptedUuencoded = uuencode(walletMaterialEncrypted)
#
#
# -- QR encode the encrypted encoded wallet material
#  # generate a filename for it
# walletMaterialEncryptedEncodedFilename = apg -a 1 -n 1 -m 16 -x 16 -M SNCL -c cl_seed -q # generates a 16 digit strong filename. check the -M setting to make sure the character set is appropriate
# qrencode -o walletMaterialDirectory/walletMaterialEncryptedEncodedFilename walletMaterialEncryptedUuencoded
#
#
#
# -- lay out page 1: encoded wallet passx and encoded paper passx
#
# page_1 = Image.new("RGB", (2550, 3300), "white")  # assuming an 8.5 x 11 page at 300 DPI, no margin, fully specified
#  #  we could also use a meow background image of some kind ??
#
#  # open files to use in this page
# walletPassxMaterialEncodedPIL     = Image.open("walletPassxMaterialDirectory/walletPassxMaterialEncodedFilename")
# paperPassxMaterialEncodedPIL      = Image.open("paperPassxMaterialDirectory/paperPassxMaterialEncodedFilename")
#
#  #lay out the page
# 
#  # it would be fun to put a meow header image here... 
#
#  # write the wallet name on all the things
# page_1.draw.text((x, y),wallet_address_string,(255,255,255),font=font) # I can imagine the instructions for this need to be wordsmithed a bit?
#
# page_1.draw.text((x, y),"This is the password to decode the QR code of the wallet file...",(255,255,255),font=font) # I can imagine the instructions for this need to be wordsmithed a bit?
# page_1.paste(walletPassxMaterialEncodedPIL, (x,y))
#
# page_1.draw.text((x, y),"This is the wallet password, to use when you are using the wallet file to make transactions...",(255,255,255),font=font) # I can imagine the instructions for this need to be wordsmithed a bit?
# page_1.paste(walletPassxMaterialEncodedPIL, (x,y))
#
#  # maybe a meow footer of some kind too
#
#
#
#
#
# -- lay out page 2: encrypted encoded ethereum wallet material printout
#  # using python image library. see http://effbot.org/imagingbook/image.htm and various other pages at the url.
#  # this is abbreviated pseudo-code but you get the idea
#
# page_2 = Image.new("RGB", (2550, 3300), "white")  # assuming an 8.5 x 11 page at 300 DPI, no margin, fully specified
#
#  # open files to use in this page
# walletMaterialEncryptedEncodedPIL = Image.open("walletMaterialDirectory/walletMaterialEncryptedEncodedFilename")
#
#  #lay out the page
# 
#  # it would be fun to put a meow header image here... 
#
#  # write the wallet name on all the things
# page_2.draw.text((x, y),wallet_address_string,(255,255,255),font=font) # I can imagine the instructions for this need to be wordsmithed a bit?
#
# page_2.draw.text((x, y),"This is the QR code of the wallet file...",(255,255,255),font=font) # I can imagine the instructions for this need to be wordsmithed a bit?
# page_2.paste(walletMaterialEncryptedEncodedPIL, (x,y))
#
#
#  # maybe a meow footer of some kind too
#
#
# -- securely delete everything you have not deleted yet
#   # you want to do this in the background while you do the printing
#   # this gives you a better chance of the process completing before things get turned off
#
# srm -r walletPassxMaterialDirectory & 
# srm -r walletMaterialDirectory $
# srm -r paperPassxMaterialDirectory &
#
#  # note there are lots of issues with srm, wipe, etc, in journalled file sywtems and ssd volumes. so this is not a solution, it is an attempt to mitigate which may be very ineffective.
#
#
# -- send the pages to the printer
#  # the way you do this is simply to 'save' them to /dev/lpr
#
#   while successPrinting = retry {
#       page_1.save("/dev/lpr")
#       page_2.save("/dev/lpr")
#   
#       splash "was print successful?" (successPrinting = yes | retry | quit)
#
#       }
#
#
#   # could it be that easy? prob not.
#
#
# -- termination
#
#  # do we need to anything else to shut down?
#  # for instance, do we need to explicitly free up variables and / or wipe memory?
#  
#  # variable deletion (not guaranteed to eliminate traces)
# Delete test_page
# Delete walletPassxMaterial
# Delete wallet_address_string
# Delete paperPassxMaterial
# Delete walletMaterialEncrypted
# Delete page_1
# Delete walletPassxMaterialEncodedPIL
# Delete paperPassxMaterialEncodedPIL
# Delete page2
# Delete walletMaterialEncryptedEncodedPIL
#
####################################################################################################
# # proposed workflow
#
# meow decode 

#
#
#




          
