#!/bin/bash
#
# Developed by Fred Weinhaus 12/24/2009 .......... revised 8/1/2021
#
# ------------------------------------------------------------------------------
# 
# Licensing:
# 
# Copyright © Fred Weinhaus
# 
# My scripts are available free of charge for non-commercial use, ONLY.
# 
# For use of my scripts in commercial (for-profit) environments or 
# non-free applications, please contact me (Fred Weinhaus) for 
# licensing arrangements. My email address is fmw at alink dot net.
# 
# If you: 1) redistribute, 2) incorporate any of these scripts into other 
# free applications or 3) reprogram them in another scripting language, 
# then you must contact me for permission, especially if the result might 
# be used in a commercial or for-profit environment.
# 
# My scripts are also subject, in a subordinate manner, to the ImageMagick 
# license, which can be found at: http://www.imagemagick.org/script/license.php
# 
# ------------------------------------------------------------------------------
# 
####
#
# USAGE: downsize [-s size] [-t toler] [-m maxiter] [-c copy] [-S strip] 
# infile outfile
# USAGE: downsize [-help]
#
# OPTIONS:
#
# -s      size	       	desired output file size in kilobytes; float>0; 
#                       default=200
# -t      toler         tolerance or allowed size of result greater than 
#                       desired size expressed as percent of desired size; 
#                       float>=0; default=10
# -m      maxiter       maximum number of iterations to stop; integer>1; 
#                       default=20
# -c      copy          copy to output when not downsizing and no image 
#                       format change; yes (y) or no (n); default=yes
# -S      strip         strip all meta data; yes (y) or no (n); default=yes
#
###
#
# NAME: DOWNSIZE 
# 
# PURPOSE: To downsize (reduce) an image to a specified file size.
# 
# DESCRIPTION: DOWNSIZE reduces an image's dimensions to achieve a specified 
# file size. For non-JPG images, processing will continue until either the 
# desired tolerance is achieved or the maximum number of iterations is reached. 
# For JPG images, processing will continue as above, but may stop when no 
# change of file size (or quality) occurs. Thus the desired file size may not 
# full be achieved to within the specified tolerance. Approximately 1% 
# tolerance is practical amount that can be achieved for non-JPG images. For 
# JPG images, the value may or may not be achieved. When strip is no, 
# processing will be skipped, if the input file size is less than or equal to 
# the combined desired file size plus the size of the meta data or if the  
# desired size is less than the meta data size.
# 
# OPTIONS: 
# 
# -s size ... SIZE is the desired output image size in kilobytes. Values are 
# floats>0. The default=200
# 
# -t toler ... TOLER is allowed size of the result within than the desire 
# size expressed as a percent of the desired size. Values are floats>=0. 
# The default=10. Processing will iterate until the resulting image size 
# is within the tolerance. If the tolerance is too low, then iterations will  
# stop when it reaches a value of maxiter. The default=10 (10%). If both toler 
# and maxiter are too small, then iteration could continue indefinitely, 
# since the algorithm may not be able to get as close as desired.
# 
# -m maxiter ... MAXITER is the maximum number of iterations to stop. Values 
# are integer>1. The default=20. If both toler and maxiter are too small, 
# then iteration could continue indefinitely, since the algorithm may not 
# be able to get as close as desired.
# 
# -c copy ... COPY will copy the input to the output when both no downsize 
# processing happens and the input and output formats are the same.
# Values are either: yes (y) or no (n). Yes means make a copy of the input 
# with the output name and no means simply skip processing and do not copy 
# The input data to the output file. The default=yes.
# 
# -S strip ... STRIP all meta data. Choices are: yes (y) or no (n). The 
# default=yes. Note that if you do not strip, the file size will be limited 
# to the size of the meta data.
#
# NOTE: Images will be converted to 8 bits/pixel/channel.
# 
# CAVEAT: No guarantee that this script will work on all platforms, 
# nor that trapping of inconsistent parameters is complete and 
# foolproof. Use At Your Own Risk. 
# 
######
#

# set default values
size=200		# desired output filesize in kilobytes
toler=10		# tolerance as percent of size; toler>=0
maxiter=20		# maximum iterations
copy="yes"		# copy to output when not downsizing if no image format change
strip="yes"		# strip meta data; yes or no
toler1=10		# initial iteration for jpg; final iteration uses toler


# set directory for temporary files
dir="."    # suggestions are dir="." or dir="/tmp"

# set up functions to report Usage and Usage with Description
PROGNAME=`type $0 | awk '{print $3}'`  # search for executable on path
PROGDIR=`dirname $PROGNAME`            # extract directory of program
PROGNAME=`basename $PROGNAME`          # base name of program
usage1() 
	{
	echo >&2 ""
	echo >&2 "$PROGNAME:" "$@"
	sed >&2 -e '1,/^####/d;  /^###/g;  /^#/!q;  s/^#//;  s/^ //;  4,$p' "$PROGDIR/$PROGNAME"
	}
usage2() 
	{
	echo >&2 ""
	echo >&2 "$PROGNAME:" "$@"
	sed >&2 -e '1,/^####/d;  /^######/g;  /^#/!q;  s/^#*//;  s/^ //;  4,$p' "$PROGDIR/$PROGNAME"
	}


# function to report error messages
errMsg()
	{
	echo ""
	echo $1
	echo ""
	usage1
	exit 1
	}


# function to test for minus at start of value of second part of option 1 or 2
checkMinus()
	{
	test=`echo "$1" | grep -c '^-.*$'`   # returns 1 if match; 0 otherwise
    [ $test -eq 1 ] && errMsg "$errorMsg"
	}

# test for correct number of arguments and get values
if [ $# -eq 0 ]
	then
	# help information
   echo ""
   usage2
   exit 0
elif [ $# -gt 12 ]
	then
	errMsg "--- TOO MANY ARGUMENTS WERE PROVIDED ---"
else
	while [ $# -gt 0 ]
		do
			# get parameter values
			case "$1" in
		     -help)    # help information
					   echo ""
					   usage2
					   exit 0
					   ;;
				-c)    # get copy
					   shift  # to get the next parameter
					   # test if parameter starts with minus sign 
					   errorMsg="--- INVALID COPY SPECIFICATION ---"
					   checkMinus "$1"
					   copy=`echo "$1" | tr '[A-Z]' '[a-z]'`
					   case "$copy" in 
					   		yes|y) copy="yes";;
					   		no|n) copy="no";;
					   		*) errMsg "--- COPY=$copy IS AN INVALID VALUE ---" 
					   	esac
					   ;;
				-s)    # get size
					   shift  # to get the next parameter
					   # test if parameter starts with minus sign 
					   errorMsg="--- INVALID SIZE SPECIFICATION ---"
					   checkMinus "$1"
					   size=`expr "$1" : '\([.0-9]*\)'`
					   sizetest=`echo "$size <= 0" | bc`
					   [ $sizetest -eq 1 ] && errMsg "--- SIZE=$size MUST BE A FLOAT GREATER THAN 0 ---"
					   ;;
				-t)    # get toler
					   shift  # to get the next parameter
					   # test if parameter starts with minus sign 
					   errorMsg="--- INVALID TOLER SPECIFICATION ---"
					   checkMinus "$1"
					   toler=`expr "$1" : '\([.0-9]*\)'`
					   tolertest=`echo "$toler < 0" | bc`
					   [ $tolertest -eq 1 ] && errMsg "--- TOLER=$toler MUST BE A NON-NEGATIVE FLOAT ---"
					   ;;
				-m)    # get maxiter
					   shift  # to get the next parameter
					   # test if parameter starts with minus sign 
					   errorMsg="--- INVALID MAXITER SPECIFICATION ---"
					   checkMinus "$1"
					   maxiter=`expr "$1" : '\([0-9]*\)'`
					   maxitertest=`echo "$maxiter < 1" | bc`
					   [ $maxitertest -eq 1 ] && errMsg "--- MAXITER=$maxiter MUST BE A POSITIVE INTEGER ---"
					   ;;
				-S)    # get strip
					   shift  # to get the next parameter
					   # test if parameter starts with minus sign 
					   errorMsg="--- INVALID STRIP SPECIFICATION ---"
					   checkMinus "$1"
					   strip=`echo "$1" | tr '[A-Z]' '[a-z]'`
					   case "$strip" in 
					   		yes|y) strip="yes";;
					   		no|n) strip="no";;
					   		*) errMsg "--- STRIP=$strip IS AN INVALID VALUE ---" 
					   	esac
					   ;;
				 -)    # STDIN and end of arguments
					   break
					   ;;
				-*)    # any other - argument
					   errMsg "--- UNKNOWN OPTION ---"
					   ;;
		     	 *)    # end of arguments
					   break
					   ;;
			esac
			shift   # next option
	done
	#
	# get infile and outfile
	infile="$1"
	outfile="$2"
fi

# test that infile provided
[ "$infile" = "" ] && errMsg "NO INPUT FILE SPECIFIED"

# test that outfile provided
[ "$outfile" = "" ] && errMsg "NO OUTPUT FILE SPECIFIED"


# setup for stripping meta data
if [ "$strip" = "yes" ]; then
	stripping="-strip"
else
	stripping=""
fi

# get file type of input
# ftypes are: JPEG, TIFF, PNG and GIF
ftype=`convert "$infile" -ping -format "%m" info:`

# get suffix of outfile
outlist=`echo $outfile | tr "." " "`
partsArray=($outlist)
numparts=${#partsArray[*]}
suffix=${partsArray[$numparts-1]}
suffix=`echo $suffix | tr "[:lower:]" "[:upper:]"`
[ "$suffix" = "JPG" ] && suffix="JPEG"
[ "$suffix" = "TIF" ] && suffix="TIFF"

# if ftype != suffix, set ftype to suffix
# IM can deal with ftype TIFF or TIF and JPEG or JPG
[ "$ftype" != "$suffix" ] && changetype="yes" || changetype="no"
[ "$ftype" != "$suffix" ] && ftype=$suffix

# if JPG, then set quality to 100
if [ "$ftype" = "JPEG" ]; then
	setquality="-quality 100"
	setunits="-units pixelsperinch"
else
	setquality=""
	setunits=""
fi

# get input compression
compression=`convert "$infile" -ping -format "%C" info:`

if [ "$ftype" = "TIFF" -a "$compresson" = "JPEG" ]; then
	setcompression="-compress none"
elif [ "$ftype" = "TIFF" -a "$compresson" != "JPEG" ]; then
	setcompression="-compress $compression"
else
	setcompression=""
fi

# if strip is no, get size of meta data in bytes
if [ "$strip" = "no" ]; then
	meta_list=`identify -verbose "$infile" | grep "Profile-" | sed 's/^[ ]*//' | cut -d\  -f2`
	meta_sum=0
	for amt in $meta_list; do
	meta_sum=$((meta_sum+amt))
	done
fi

# set up temp file
tmpA1="$dir/downsize_1_$$.$suffix"

trap "rm -f $tmpA1;" 0
trap "rm -f $tmpA1; exit 1" 1 2 3 15
#trap "rm -f $tmpA1; exit 1" ERR

# read the input image into the temp files and test validity.
convert -quiet "$infile"[0] $stripping -depth 8 $setcompression $setquality $setunits +repage ${ftype}:$tmpA1 ||
	errMsg "--- FILE $infile DOES NOT EXIST OR IS NOT AN ORDINARY FILE, NOT READABLE OR HAS ZERO SIZE  ---"

# get filesize
# fullsize is converted to bytes
# size2 is size converted to bytes
test1=`convert $tmpA1 -ping -format "%b" info:- | grep "MB"`
test2=`convert $tmpA1 -ping -format "%b" info:- | grep "KB"`
test3=`convert $tmpA1 -ping -format "%b" info:- | grep "B"`
fullsize=`convert -ping $tmpA1 -format "%b" info: | tr -d "[:alpha:]"`
if [ "$test1" != "" ]; then
	fullsize=`convert xc: -format "%[fx:$fullsize*1000000]" info:`
elif [ "$test2" != "" ]; then
	fullsize=`convert xc: -format "%[fx:$fullsize*1000]" info:`
elif [ "$test3" != "" ]; then
	fullsize=$fullsize
else
	errMsg="--- UNRECOGNIZED FILESIZE SUFFIX ---"
fi
size2=`convert xc: -format "%[fx:$size*1000]" info:`
#echo "test1=$test1; test2=$test2; test3=$test3; ftype=$ftype; fullsize=$fullsize; size2=$size2;"

# process image for strip=yes, if input size > desired size
# process image for strip=no, if input size > desired size + meta size 
# and the desired size is greater than the meta size
if [ "$strip" = "yes" ]; then
	test4=`convert xc: -format "%[fx:($fullsize>$size2)?1:0]" info:`
elif [ "$strip" = "no" ]; then
	test4=`convert xc: -format "%[fx:($fullsize>$size2+$meta_size) && ($size2>=$meta_size)?1:0]" info:`
	size2=$((size2+meta_size))
fi

if [ $test4 -eq 1 ]; then
	# iterate
	i=1
	diffsize=0
	iterate=1
	newsize=$fullsize
	if [ "$ftype" = "JPEG" ]; then
		# iterate from previous image to new image as outfile
		# this may give blurry results but close values
		# so get the final images size and resize one last time from the original
		# also use -define jpeg:extent=${size}KB which will change the quality to get closer
		# if used the alternate method below with JPEG, sometimes got overshoots and pratio=nan since newsize became negative
		convert $tmpA1 "$outfile"
		while [ $iterate -eq 1 -a $i -lt $maxiter ]; do
			# get sqrt size ratio in percent
			pratio=`convert xc: -format "%[fx:100*sqrt($size/$newsize)]" info:`
			#echo "i=$i; fullsize=$fullsize; size=$size; size2=$size2; newsize=${newsize}kB; pratio=$pratio;"
		
			# resize image
			convert "$outfile" -resize ${pratio}% -depth 8 $setquality $setunits ${ftype}:"$outfile"
		
			# set newsize in KB
			testa=`convert "$outfile" -ping -format "%b" info:- | grep "MB"`
			testb=`convert "$outfile" -ping -format "%b" info:- | grep "KB"`
			testc=`convert "$outfile" -ping -format "%b" info:- | grep "B"`
			if [ "$testa" != "" ]; then
				newsize=`convert "$outfile" $setquality ${ftype}:- | convert - -format "%b" info: | tr -d "[:alpha:]"`
				newsize=`convert xc: -format "%[fx:$newsize*1000]" info:`
			elif [ "$testb" != "" ]; then
				newsize=`convert "$outfile" $setquality ${ftype}:- | convert - -format "%b" info: | tr -d "[:alpha:]"`
			elif [ "$testc" != "" ]; then
				newsize=`convert "$outfile" $setquality ${ftype}:- | convert - -format "%b" info: | tr -d "[:alpha:]"`
				newsize=`convert xc: -format "%[fx:$newsize/1000]" info:`
			fi		
			echo "i=$i newsize=${newsize}kB quality=100"
			diffsize=`convert xc: -format "%[fx:($newsize-$size)]" info:`
			iterate=`convert xc: -format "%[fx:abs($diffsize)>($toler1*$size/100)?1:0]" info:`
			#echo "PART1: i=$i; newsize=${newsize}kB; diffsize=$diffsize; iterate=$iterate;"
			i=$(($i+1))
		done

		# get final size of iterated outfile and then use that to resize the original
		dim=`convert "$outfile" -format "%wx%h" info:`
		convert $tmpA1 -resize $dim -define jpeg:extent=${size}KB -depth 8 $setquality $setunits ${ftype}:"$outfile"
		# set newsize in KB
		testa=`convert "$outfile" -ping -format "%b" info:- | grep "MB"`
		testb=`convert "$outfile" -ping -format "%b" info:- | grep "KB"`
		testc=`convert "$outfile" -ping -format "%b" info:- | grep "B"`
		oldsize=$newsize
		if [ "$testa" != "" ]; then
			newsize=`convert -ping "$outfile" -format "%b" info: | tr -d "[:alpha:]"`
			newsize=`convert xc: -format "%[fx:$newsize*1000]" info:`
		elif [ "$testb" != "" ]; then
			newsize=`convert -ping "$outfile" -format "%b" info: | tr -d "[:alpha:]"`
		elif [ "$testc" != "" ]; then
			newsize=`convert -ping "$outfile" -format "%b" info: | tr -d "[:alpha:]"`
			newsize=`convert xc: -format "%[fx:$newsize/1000]" info:`
		fi		
		quality=`convert -ping "$outfile" -format "%Q" info:`
		echo "i=$i newsize=${newsize}kB quality=$quality"
		diffsize=`convert xc: -format "%[fx:($size-$newsize)]" info:`
		#newsign=`convert xc: -format "%[fx:sign($size-$newsize)]" info:`
		#oldsign=$newsign
		size1=`convert xc: -format "%[fx:$size+$diffsize]" info:`
		iterate=`convert xc: -format "%[fx:abs($diffsize)>($toler*$size/100)?1:0]" info:`
		#echo "PART2: i=$i; newsign=$newsign; oldsign=$oldsign; quality=$quality; size1=${size1}KB; newsize=${newsize}KB; diffsize=$diffsize; iterate=$iterate;"
		i=$((i+1))
		
		# iterate again changing jpeg write extent size
#		while [ $iterate -eq 1 -a $i -lt $maxiter -a $newsign -eq $oldsign -a "$newsize" != "$oldsize" ]; do
		while [ $iterate -eq 1 -a $i -lt $maxiter -a "$newsize" != "$oldsize" ]; do
			convert $tmpA1 -resize $dim -define jpeg:extent=${size1}KB -depth 8 $setquality $setunits ${ftype}:"$outfile"
			# set newsize in KB
			testa=`convert "$outfile" -ping -format "%b" info:- | grep "MB"`
			testb=`convert "$outfile" -ping -format "%b" info:- | grep "KB"`
			testc=`convert "$outfile" -ping -format "%b" info:- | grep "B"`
			oldsize=$newsize
			if [ "$testa" != "" ]; then
				newsize=`convert -ping "$outfile" -format "%b" info: | tr -d "[:alpha:]"`
				newsize=`convert xc: -format "%[fx:$newsize*1000]" info:`
			elif [ "$testb" != "" ]; then
				newsize=`convert -ping "$outfile" -format "%b" info: | tr -d "[:alpha:]"`
			elif [ "$testc" != "" ]; then
				newsize=`convert -ping "$outfile" -format "%b" info: | tr -d "[:alpha:]"`
				newsize=`convert xc: -format "%[fx:$newsize/1000]" info:`
			fi
			quality=`convert -ping "$outfile" -format "%Q" info:`
			echo "i=$i newsize=${newsize}kB quality=$quality"
			diffsize=`convert xc: -format "%[fx:($size-$newsize)]" info:`
			#oldsign=$newsign
			#newsign=`convert xc: -format "%[fx:sign($size-$newsize)]" info:`
			size1=`convert xc: -format "%[fx:0.5*($size+$newsize)]" info:`
			iterate=`convert xc: -format "%[fx:abs($diffsize)>($toler*$size/100)?1:0]" info:`
			#echo "PART3: i=$i; newsign=$newsign; oldsign=$oldsign; quality=$quality; size1=${size1}KB; newsize=${newsize}KB; diffsize=$diffsize; iterate=$iterate;"
			i=$(($i+1))
		done

		

	else
		while [ $iterate -eq 1 -a $i -lt $maxiter ]; do
			# get sqrt size ratio in percent
			size2=`convert xc: -format "%[fx:max($size2-($diffsize*1000),0)]" info:`
			pratio=`convert xc: -format "%[fx:100*sqrt($size2/$fullsize)]" info:`
			#echo "i=$i; fullsize=$fullsize; size=$size; size2=$size2; pratio=$pratio;"
			
			testd=`convert xc: -format "%[fx:$size2<($toler*$size/100)?1:0]" info:`
			[ $testd -eq 1 ] && break
		
			# resize image
			convert $tmpA1 -resize ${pratio}% -depth 8 $setcompression $setquality $setunits ${ftype}:"$outfile"
			printsize=`convert "$outfile" -ping -format "%b" info:`
			echo "i=$i; size=${printsize}"
						
			testa=`convert "$outfile" -ping -format "%b" info:- | grep -i "MB"`
			testb=`convert "$outfile" -ping -format "%b" info:- | grep -i "KB"`
			testc=`convert "$outfile" -ping -format "%b" info:- | grep -i "B"`
			if [ "$testa" != "" ]; then
				newsize=`convert "$outfile" -depth 8 $setcompression $setquality $setunits ${ftype}:- | convert - -ping -format "%b" info: | tr -d "[:alpha:]"`
				newsize=`convert xc: -format "%[fx:$newsize*1000]" info:`
			elif [ "$testb" != "" ]; then
				newsize=`convert "$outfile" -depth 8 $setcompression $setquality $setunits ${ftype}:- | convert - -ping -format "%b" info: | tr -d "[:alpha:]"`
			elif [ "$testc" != "" ]; then
				newsize=`convert "$outfile" -depth 8 $setcompression $setquality $setunits ${ftype}:- | convert - -ping -format "%b" info: | tr -d "[:alpha:]"`
				#newsize=`convert xc: -format "%[fx:$fullsize/1000]" info:`
				newsize=`convert xc: -format "%[fx:$newsize/1000]" info:`
			fi		
			#echo "i=$i; newsize=${newsize}kB"
			diffsize=`convert xc: -format "%[fx:($newsize-$size)]" info:`
			iterate=`convert xc: -format "%[fx:abs($diffsize)>($toler*$size/100)?1:0]" info:`
			#echo "i=$i; newsize=${newsize}kB; diffsize=$diffsize; iterate=$iterate;"
			i=$(($i+1))
		done
	fi
	
elif [ "$changetype" = "no" -a "$copy" = "yes" ]; then
	convert "$infile" "$outfile"

else
	convert $tmpA1 -depth 8 $setcompression $setquality $setunits "$outfile"
fi

finalsize=`convert "$outfile" -format "%b" info:`
echo "final size = $finalsize"

exit
