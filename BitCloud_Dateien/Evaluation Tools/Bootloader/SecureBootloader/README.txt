=================================== README ======================================
#*******************************************************************************#
#                                                                               #
#       This tool will generate an encrypted image from an srec file            #
#       Encryption Type : AES-128 CBC                                           #
#                                                                               #
#       USAGE:encrypt_bc.exe <configfile>                                       #
#                                                                               #
#============================CONFIG FILE FORMAT=================================#
#                                                                               #
#       DEVICE_TYPE=SAMR21                                                      #
#       CYPHERKEY = 1,18,35,52,69,86,103,120,137,144,153,136,119,102,85,68      #
#       IV = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0                                    #
#       INPUT_SREC_FILE=boot_loader_input.srec                                  #
#       OTA_HEADER_FILE=ota_header.bin                                          #
#       IMAGETYPE_BITS_15_12=1100                                               #
#                                                                               #
#===============================================================================#
#                                                                               #
#       Note : Expects InputFile and other executables in the same directory    #
#       Note : Reqd Files:<Objcopy.exe> <calc_crc.exe> <srecfile> <ota hdr_file>#
#       Note : Convert the binary to srec(s28 format) using objcopy             #
#       Note : If above step gives s19 fmt,convert s19 to s28                   #
#       Note : Device Type : SAMR21 / MEGARF                                    #
#       *PLEASE NOTE TOOL WILL DELETE GENERATED TEMP FILES(*INPUT_SREC*.bin)*   #
#                                                                               #
#*******************************************************************************#

  Input SREC File ->  <Tool:objcopy><Out:RawFile>  ->  Encrypt -> Add Ota header -> <MAC Encrpyt(if bit Enabled)> <Calc CRC and Encrypt (if Enabled)>  -> Update Size to header -> <Tool:objcopy><Out:Srec File>