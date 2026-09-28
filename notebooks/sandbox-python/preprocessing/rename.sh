#!/bin/sh

module load nco

ncrename -v fld_s00i024,ts -v fld_s01i201,ssrc -v fld_s01i207,rsdt -v fld_s01i208,rsut -v fld_s02i201,str -v fld_s02i205,rlut -v fld_s03i217,hfss -v fld_s03i234,hfls -v fld_s05i216,pr -v fld_s16i222,psl -v fld_s30i201,u -v fld_s30i202,v -v fld_s30i204,ta -v fld_s30i205,hus -v fld_s30i207,zg -v fld_s30i208,omega -v fld_s30i301,heaviside -v fld_s02i206,rlutcs -v fld_s01i209,rsutcs -v fld_s03i236,tas -v fld_s03i392,tauu cm3_PD-control_1981-2030.nc

#ncrename -v fld_s02i206,rlutcs -v fld_s01i209,rsutcs atmos_fields_000-174_NovSpinUp.nc
#ncrename -v fld_s03i261,gpp -v fld_s03i262,npp -v fld_s03i293,rh -v fld_s03i236,tas carbon_fields_331-864_junespinup.nc

#ncrename -v fld_s02i284,sulphateAOD -v fld_s02i285,mineraldustAOD -v fld_s02i286,seasaltAOD -v fld_s02i287,sootAOD -v fld_s02i288,biomassAOD dust_fields_331-864_junespinup.nc

