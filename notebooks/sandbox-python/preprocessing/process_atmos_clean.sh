#!/bin/sh



while IFS= read -r line; do
##parse
	first=$(echo $line |  sed 's/.*output//') 
	yr=$(echo $first \ | grep -o '[0-9]\{6\}')
        echo ${yr}

	cdo selname,fld_s00i024,fld_s16i222,fld_s05i216,fld_s02i205,fld_s01i207,fld_s01i208,fld_s01i201,fld_s02i201,fld_s03i217,fld_s03i234,fld_s30i201,fld_s30i202,fld_s30i208,fld_s30i204,fld_s30i205,fld_s30i207,fld_s30i301,fld_s02i206,fld_s01i209,fld_s03i236,fld_s03i392 $line tmp/${yr}

# some carbon and dust fields
#	cdo selname,fld_s02i284,fld_s02i285,fld_s02i286,fld_s02i287,fld_s02i288 $line tmp/${yr}_${mon}_dust
#	cdo selname,fld_s03i261,fld_s03i262,fld_s03i293,fld_s03i236 $line tmp2/${yr}_${mon}_carbon

done < 'filenames_cm3_PD-control'
