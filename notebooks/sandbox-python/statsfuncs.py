"""
 Python functions, mostly written by Harun Rashid (harun.rashid@csiro.au). Not all functions
 are well tested. No warranty is provided; use these functions at your own risk.
Bug reports to: harun.rashid@csiro.au
"""

import sys
import numpy as np
import scipy as sp
import numpy.linalg
import scipy.linalg
import scipy.stats
import pandas as pd

def move_list_item(list_name, item_name, pos):
    """Moves item_name (string/int) to position pos (int) of a python list list_name.
    """
    if item_name in list_name and list_name[pos] != item_name:
        list_name.remove(item_name)
        list_name.insert(pos,item_name)
        return list_name
    else:
        print(item_name+" doesn't exist in list or it is already in place!")
        return

def move_column_inplace(df, col, pos):
    """Moves column col (string/int) to position pos (int) of a pandas DataFrame df.
    """
    col = df.pop(col)
    df.insert(pos, col.name, col)

def center(x, axis=0):
    """Return x minus its mean along the specified axis. Taken from
    pylab.
    """
    x = np.asarray(x)
    if axis == 0 or axis is None or x.ndim <= 1:
        return x - x.mean(axis)
    ind = [slice(None)] * x.ndim
    ind[axis] = np.newaxis
    return x - x.mean(axis)[ind]

def copy_varMeta (fld1,fld2):
    """Copies attributes and coordinate info from from one xr.DataArray (fld1) to a numpy
    or xr.DataArray (fld2). Both arrays must have the same shape (not checked).
    """
    import xarray as xr

    if not isinstance(fld1,xr.DataArray):
        print('fld1 must be an xarray DataArray()!')
        return

    if isinstance(fld2,np.ndarray):
        fld = xr.DataArray(fld2,dims=fld1.dims,coords=fld1.coords)
    else:
        fld = fld2.copy()
    for k,v in fld1.attrs.items():
        fld.attrs[k] = v

    return fld
 
def trend(h, t=None, nord=1, tline=False):
   """Returns slope (p[0]) and intercept (p[1]) of linear trend in h (t=False). If the
   independent variable t is provided, the regression coefficient(s) of h onto t are
   returned. h can be 1-d or more, but t must be 1-d.

   If nord>1, p[0:nord] are coeffcients and p[-1] is the intercept.

   Calculate and return trendline if tline=True:
      h_est = p[0]*t + p[1]    # plot as: plt.plot(t, h_est); see also func regline below
   """ 
   n = len(h)
   if t is None:
       t = np.arange(n)
   idx = np.isfinite(h) & np.isfinite(t)
   p = np.polyfit(t[idx], h[idx], nord)
   if tline and nord==1:
       trend_line = p[0]*t + p[1]
       return p, trend_line
   else: 
       return p

def trend_df(h, t=None, nord=1, tline=False):
   """Returns slope (p[0]) and intercept (p[1]) of linear trend in h (t=False). If the
   independent variable t is provided, the regression coefficient(s) of h onto t are
   returned. h can be 1-d or more, but t must be 1-d.

   If nord>1, p[0:nord] are coeffcients and p[-1] is the intercept.

   Calculate and return trendline if tline=True:
      h_est = p[0]*t + p[1]

   This function is for a pandas dataframe. Use da.polyfit() for xarray objects.
   """ 

   if isinstance(h,pd.DataFrame):
       ensm = h.columns
   else:
       print('trend_df is for a pandas dataframe! Use "trend" or "regline" function')
       return

   df_trend = h.apply(lambda y: trend(y,t=t,nord=nord)) # same as below but simpler
   #df_trend = pd.DataFrame({r:trend(h[r],t=t,nord=nord) for r in ensm},index=['slope','intcept'])
   if tline:
       if t is None: t = np.arange(1,h.shape[0]+1)
       df_trend = df_trend.apply(lambda x: x[0]*t+x[1])
   else:
       df_trend.index = ['slope','intcept']
   return df_trend

def regline(x, y):
   """Returns the straight-line fit for x & y, by linear regression analysis of y 
   onto x. x and y both must be 1-d.
   """ 

   p, tl = trend(y, x, tline=True)
   if isinstance(tl,pd.Series):
       tl.index = x
   else:
       tl = pd.Series(tl, index=x)
   return tl.sort_index()

def detrend(h, nord=1): 
   n = len(h)
   t = np.arange(n)
   idx = np.isfinite(h)
   p = np.polyfit(t[idx], h[idx], nord) 
   h_detrended = h - np.polyval(p, t) 
   return h_detrended

def detrend_df(h, nord=1): 
   """Detrend a dataframe column-wise. A 2-d h must be a pandas dataframe.
   """
   if len(h.shape) == 1:
       return detrend(h, nord=nord)
   else:
       return h.transform(lambda x: detrend(x,nord=nord))

def detrend_xr(da, dim, nord=1):
    # detrend along a single dimension (xarray only?)
    import xarray as xr
    p = da.polyfit(dim=dim, deg=nord)
    fit = xr.polyval(da[dim], p.polyfit_coefficients)
    return da - fit

def curvefit_sr (h, nord=3):
   """Fit a nord order curve to 1-d array h(t). This function is for a 1-d numpy/pandas
   object.
   """ 
   n = len(h)
   t = np.arange(n)
   idx = np.isfinite(h)
   p = np.polyfit(t[idx], h[idx], nord) 
   return np.polyval(p, t)+h-h  # extra operations to return pandas obj (is there a better way?)

def curvefit2 (h, t=None, nord=2):
   """Fit a nord order curve for 1-d array h(t) onto t (independent variable). This function 
   is for 1-d numpy/pandas objects. See, xr.DataArray.curvefit() for xr multi-dim arrays.

   This is equivalent to the following code:
     df_res2 = regResid1(t, h, nord=2)
     df_fit2 = h-df_res2
     df_fit2.index = t.values
     df_fit2.sort_index()   # same as df_hfit.sort_index() below
   """ 
   n = len(h)
   if t is None:
       t = np.arange(n)
   idx = np.isfinite(h) & np.isfinite(t)
   p = np.polyfit(t[idx], h[idx], nord)
   df_hfit = pd.Series(np.polyval(p, t),index=t) 
   return df_hfit.sort_index()

def curvefit (h, nord=3):
   """Fit a nord order curve to 1-d array h(t). This function is for 1- or 2-d numpy/pandas
   objects.
   """

   if np.ndim(h) == 1:
       return curvefit_sr (h, nord=nord)
   elif np.ndim(h) == 2:
       return h.apply(lambda x: curvefit_sr (x, nord=nord))

def extrap (df0, nord=3):
    """Extrapolation (and interpolation) of a dataframe/series with missing boundary values
    by a polynomial/curve fit. Note, nord=0 returns a linearly interpolated array.

    Example usage:

    import numpy as np
    import pandas as pd
    import mystats as ms
    import matplotlib.pyplot as plt

    df_x1 = pd.Series([np.nan,1.,2.3,np.nan,5.1,np.nan,0.5,np.nan,np.nan])

    df_x4 = pd.concat([ms.extrap(df_x1,nord=0), ms.extrap(df_x1,nord=1), ms.extrap(df_x1,nord=2),\
                   ms.extrap(df_x1,nord=3),df_x1],axis=1)
    df_x4.columns = ['Linear','nord=1','nord=2','nord=3','Original']

    df_x4.plot(style='o-',color=['blue','orange','green','red','black'])
    plt.grid()
    plt.title('Test of interpolation/extrapolations with different orders\n using ms.extrap()')
    plt.show()

    16-JUL-2025     
    """

    if isinstance(df0,pd.Series):
        df = df0.to_frame()
    elif isinstance(df0,pd.DataFrame):
        df = df0.copy()
    else:
        print("Input must be pd.Series or pd.DataFrame!")
        return

    # Create copy of data to remove NaNs for curve fitting
    df.index = np.arange(len(df0.index))
    x2 = df.index
    df1 = df.copy()
    #fit_df = df.dropna()

    # Curve fit each column
    for col in df.columns:
        # Get x & y
        idx = df[pd.isnull(df[col])].index
        ndx = df[pd.notnull(df[col])].index
        x = ndx
        y = df.loc[ndx,col].values
        #idx = np.isfinite(y) # not needed, because of dropna() above
        # Curve fit column and get curve parameters
        if nord == 0:   # Linear interpolation, with forward and backfilled missing values
            df[col] = np.interp(x2,x,y)
        else:
            params = np.polyfit(x, y, nord)  # fit a function
            df[col] = np.polyval(params, x2) # Extrapolate those points with the fitted function
        df1.loc[idx,col] = df.loc[idx,col].astype('float32')

    df1.index = df0.index

    return df1

def polyintp_sr (h, g, t=None, nord=3):
   """Interpolation of 1-d array h(t) to a new independent variable g, through a polynomial fit
   of order "nord". h must be 1-d.

   When g == h.index, this function just does the nord-order polynomial fit without
   interpolation.

   When h is not a pd.Series, then t-values must be provided.
   """

   # If not a pandas DF, then convert to numpy

   if np.ndim(h) == 1:
       if isinstance(h,pd.Series):
           t = h.index
       elif t is None:
           print("t-values must be given when h is not a pd.Series!")
           return
   else:
       print("h must be a 1-d array!")
       return

   idx = np.isfinite(h)
   p = np.polyfit(t[idx], h[idx], nord)
   #p = np.polyfit(t, h, nord)
   h_int = np.polyval(p, g) 
   return pd.Series(h_int,index=g)

def polyintp (h, g, t=None, nord=3):
   """Interpolation of function h(t) to a new independent variable g, through a polynomial fit
   of order "nord". h must be 1-d or 2-d.

   When g == h.index, this function just does the nord-order polynomial fit without
   interpolation.

   When h is not a pd.Series/DataFrame, then t-values must be provided.
   """

   # If not a pandas DF, then convert to numpy

   if np.ndim(h) == 1:
       return polyintp_sr (h, g, t=t, nord=nord)
   elif np.ndim(h) == 2:
       if isinstance(h,pd.DataFrame):
           return h.apply(lambda x: polyintp_sr (x, g, t=t, nord=nord))
       else:
           if t is None:
               print("t-values must be given when h is not a pd.DataFrame/Series!")
               return
           h = pd.DataFrame(h,index=t)
           return h.apply(lambda x: polyintp_sr (x, g, t=t, nord=nord))
   else:
       print("h must be 1- and 2-d np/pd arrays!")
       return

def surfArea (lat1, lat2, R=6371.0):
   """Calculate the surface area (sq. km) between two latitude circles (lat1 > lat2).
   The formula is:
         A = 2*pi*R*R*(sin(lat1)-sin(lat2))

   where, R is earth's radius (km) and lat1 and lat2 are in deg.

   Test against the total surface area with the analytical result (4*pi*r**2)
         SurfArea = 4.*pi*R**2
   """

   if lat2>lat1:
       lat1,lat2 = lat2,lat1
   return 2*np.pi*R*R*(np.sin(np.deg2rad(lat1))-np.sin(np.deg2rad(lat2)))

def regResid1 (x, y, nord=1):
   """A function to calculate the residual y (dependent variable), 
   after removing from it the portion linearly related to x
   (independent variable). In other words, this function
   calculates the residual (e.g., for nord=1), resid = y - yhat, where 
               yhat = b*x + a,
   and b is the regression coeffient and a is the y-intercept (returned as p = [b,a]),
   given by (yave - b*xave). So the residual is given by,
               resid = y - yave - b*(x - xave)

   This function also allows for removing a > 1 deg polynomial fit, as opposed to
   regResid further below which works for nord=1 only.

   Reference: D. Wilks (1995), page 160.

   28-SEP-2020   Harun Rashid
   """

   idx = np.isfinite(x) & np.isfinite(y)
   p = np.polyfit(x[idx], y[idx], nord) 
   y_detrended = y - np.polyval(p, x) 
   return y_detrended

def regResid_nord (x, y, nord=1):
    """
    Remove the effects of a 1-d or rank(y)-d time series (x, independant variable) from 
    an upto 3-d array (y, dependant variable). Time must be the first dimension in y. Accepts
    numpy/pandas/xarray inputs.

    This function also allows for removing a > 1 deg polynomial fit, as opposed to
    regResid further below which works for nord=1 only. But this function is slower than regResid
    even for nord=1.
    """

    # If not a pandas DF, then convert to numpy

    if isinstance(y,pd.DataFrame) or isinstance(y,pd.Series):
        return y.transform(lambda h: regResid1(x,h))
    #    yp = y
    #    lp = True
    #else:
    #    lp = False

    y = np.array(y)
    x = np.array(x)

    shapex = x.shape
    shapey = y.shape
    rankx  = x.ndim
    ranky  = y.ndim
 
    if rankx not in [1,ranky] or shapex[0] != shapey[0]:
       print("x must be 1- or "+str(ranky)+"-d and/or time isn't the 1st dim in y")
       #sys.exit()
       return

    #For numpy/xarray arrays; is there a faster way than looping?

    if rankx == 1 and ranky == 1:
       yprime = regResid1 (x, y, nord)
    if ranky == 2:
       shape = y.shape[1]
       yprime = np.zeros(y.shape)
       for i in range(shape):
          if rankx == 1:
             yprime[:,i] = regResid1(x,y[:,i],nord)
          elif rankx == ranky:
             yprime[:,i] = regResid1(x[:,i],y[:,i],nord)
    elif ranky == 3:
       shape = y.shape[1:]
       yprime = np.zeros(y.shape)
       for i in range(shape[0]):
          for j in range(shape[1]):
             if rankx == 1:
                yprime[:,i,j] = regResid1(x,y[:,i,j],nord)
             elif rankx == ranky:
                yprime[:,i,j] = regResid1(x[:,i,j],y[:,i,j],nord)

    #if lp:
    #   if isinstance(yp,pd.DataFrame):
    #      yprime = pd.DataFrame(yprime,index=yp.index,columns=yp.columns)
    #   elif isinstance(yp,pd.Series):
    #      yprime = pd.Series(yprime,index=yp.index)

    return yprime

def quadwin(n): 
   """
   Quadratic (or "Welch") window
   """
   t = np.arange(n)
   win = 1 - ((t - 0.5 * n) / (0.5 * n)) ** 2 
   return win

def taper(n,fr=0.1,window='hanning'): 
   """
   Window to taper fr/2 on both sides, with 'hanning' (default) or 'blackman' windows
   """

   if window.lower()=='welch':
      return quadwin(n)

   nfrh = int(n*fr/2)
   t = np.ones(n,dtype=float)
   if window.lower()=='blackman':
      wnf = np.blackman(2*nfrh)
   else:
      wnf = np.hanning(2*nfrh)
   t[0:nfrh] = t[0:nfrh]*wnf[0:nfrh]
   t[-nfrh:] = t[-nfrh:]*wnf[nfrh:]
   return t

def crosscorr0(datax, datay, lag=0):
    """ Lag-N cross correlation. Not tested; use crosscorr() below.
    Parameters
    ----------
    lag : int, default 0
    datax, datay : pandas.Series objects of equal length

    Returns
    ----------
    crosscorr0 : float

    Usage (cross correlations at each month):
      xcov_monthly = [crosscorr0(datax, datay, lag=i) for i in range(12)]

    Compare results with crosscorr() below.
    """

    #datax = center(datax)  # converts to np arrays
    #datay = center(datay)
    datax = datax - datax.mean()
    datay = datay - datay.mean()
    return datax.corr(datay.shift(lag))

def lagcorr0(x,y,nlag=None,verbose=False):
    '''Compute lead-lag correlations between 2 time series. Not tested; use lagCorr1() below.
 
    <x>,<y>: 1-D time series.
    <lag>: lag option, could take different forms of <lag>:
          if 0 or None, compute ordinary correlation and p-value;
          if positive integer, compute lagged correlation with lag
          upto <lag>;
          if negative integer, compute lead correlation with lead
          upto <-lag>;
          if pass in an list or tuple or array of integers, compute
          lead/lag correlations at different leads/lags.
 
    Note: when talking about lead/lag, uses <y> as a reference.
    Therefore positive lag means <x> lags <y> by <lag>, computation is
    done by shifting <x> to the left hand side by <lag> with respect to
    <y>.
    Similarly negative lag means <x> leads <y> by <lag>, computation is
    done by shifting <x> to the right hand side by <lag> with respect to
    <y>.
 
    Return <result>: a (n*2) array, with 1st column the correlation
    coefficients, 2nd column correpsonding p values.
 
    Currently only works for 1-D arrays.

    Source: http://stackoverflow.com/questions/9382207/specify-lag-in-np.correlate

    '''
 
    from scipy.stats import pearsonr

    lag = nlag
    x = center(x)
    y = center(y)
    if len(x)!=len(y):
        raise('Input variables of different lengths.')
 
    #--------Unify types of <lag>-------------
    if np.isscalar(lag):
        if abs(lag)>=len(x):
            raise('Maximum lag equal or larger than array.')
        if lag<0:
            lag=-np.arange(abs(lag)+1)
        elif lag==0:
            lag=[0,]
        else:
            lag=np.arange(lag+1)   
    elif lag is None:
        lag=[0,]
    else:
        lag=np.asarray(lag)
 
    #-------Loop over lags---------------------
    result=[]
    if verbose:
        print('\n#<lagcorr>: Computing lagged-correlations at lags:',lag)
 
    for ii in lag:
        if ii<0:
            result.append(pearsonr(x[:ii],y[-ii:]))
        elif ii==0:
            result.append(pearsonr(x,y))
        elif ii>0:
            result.append(pearsonr(x[ii:],y[:-ii]))
 
    result=np.asarray(result)
 
    #return result            # y (x) leads at +ve (-ve) lag values             
    return result[::-1,:]     # x (y) leads at +ve (-ve) lag values (as in xcorr.ncl)

def xcorr(x,y=None,nlag=0):
    """Calculates auto- or cross-correlation function. This calculates the function for full
    lag values. Hence, this is faster than lagcorr (~26) for large nlags only. For smaller 
    nlag values, lagcorr is faster. But, this is still slightly faster for auto-corr (i.e.,
    y = None).
    
    Use crosscorr(), instead of this function.
    """
    xp = (np.array(x) - np.mean(x))/np.std(x)
    if y is None:
        yp = xp
    else:
        yp = (np.array(y) - np.mean(y))/np.std(y)
    result = np.correlate(xp, yp, mode='full')
    nh = len(result)//2
    if y is None:   # Auto-corr
        return result[nh:nh+nlag+1]/len(xp)
    else:
        return result[nh-nlag:nh+nlag+1]/len(xp)

def lagCorr1(x0,y0,nlag=0,missval=True):
    '''Compute lead-lag correlations between 2 time series. This function
    uses the "lagmat" and "corrcoef" functions and is 10 times faster than
    "lagcorr0" above (the latter also computes p-values). 
    
    Works for arrays with or without missing values (unlike the other corr
    functions in this module).

    Harun Rashid 14-July-2016
    '''

    from statsmodels.tsa.tsatools import lagmat

    lag = nlag
    if not np.isscalar(lag):
       lag = np.max(lag)

    if missval:
        idx = np.isfinite(x0) & np.isfinite(y0)
        x = center(x0[idx])
        y = center(y0[idx])
    else:
        x = center(x0)
        y = center(y0)

    xl=lagmat(x,maxlag=lag,trim='backward',original='in')
    yl=lagmat(y,maxlag=lag,trim='backward',original='in')
    #xl[xl==0.]=np.nan    # problematic; sets valid 0's to NaN also
    #yl[yl==0.]=np.nan

    xyl = np.concatenate((xl,yl[:,::-1]),axis=1) # put side-by-side 
    xy_corr = np.corrcoef(xyl,rowvar=0)          # 0-axis is time
    lag_corrs = np.concatenate((xy_corr[lag+1,:lag],xy_corr[lag,lag+1:]))

    return pd.Series(lag_corrs, index=np.arange(-lag,lag+1,1))

    #xyl_df = pd.DataFrame(xyl,columns=['xl2','xl1','xl0','yl0','yl1','yl2'])
    #xy_corr2 = xyl_df.corr()

def extvecback(x,lag=2):
    '''Computes the backward extended vector or matrix (lagged matrix), 
    similar to my MATLAB function of the same name.

        x => A 1-d vector or 2-d matrix, with time as dim 1
        lag => Lag or window length

    Harun Rashid 15-SEP-2016
    '''

    from statsmodels.tsa.tsatools import lagmat
    xl = lagmat(x,maxlag=lag,trim='backward',original='in')

    if lag == 0:
       return xl
    else:
       return xl[:-lag]

def extvec(x,lag=2):
    '''Computes the forward extended vector or matrix (lagged matrix), 
    similar to my MATLAB function of the same name.

        x => A 1-d vector or 2-d matrix, with time as dim 1
        lag => Lag or window length

    Harun Rashid 15-SEP-2016
    '''

    from statsmodels.tsa.tsatools import lagmat

    x = np.array(x)         # make sure it's a np.array
    if x.ndim > 2:
       print("EXTVEC: Only 1- or 2-d arrays are handled!")
       return
    elif x.ndim == 1:
       x = x[:,np.newaxis]

    x = np.fliplr(x)
    xl = lagmat(x,maxlag=lag,trim='backward',original='in')

    if lag == 0:
       return np.fliplr(xl)
    else:
       return np.fliplr(xl[:-lag])

#from random import random
#from pandas import DataFrame
#from statsmodels.api import OLS
#lr = lambda : [random() for i in range(8)]
#x = DataFrame({'x1': lr(), 'x2':lr(), 'x3':lr()})
#
#xl = ms.extvec(x,2)
#xb = ms.extvecback(x,2)

def propagator3(v, pord=1):
    '''
    USAGE: Amat,Cw,Bmat = propagator3(v, pord)
    PROPAGATOR  Estimates the propagator and system matrix.

    This PYTHON function estimates the propagator and system matrix,
      given a data array, v(nt,nx), each row of which represents a
      "map" at a particular instance. The columns represent timeseries
      at individual grid points, or of individual modes. The data
      array is assumed to be the solution of vector linear equations
      of the form:
                     dv
                    ----  = Bmat*v + F_wn        .............. (1)
                     dt
      or
                     v(t+tau) = Amat*v(t) + F_wn(t+tau) ........(2)

    INPUT:
            v -> Input data array from which the matrices to be estimated
            pord -> Order of the propagator to be fitted (order of VAR model)
            nlag -> Number of lags for lagged covariance matrix (=pord)

    OUTPUT:
            Amat -> Propagator of Eq.(2)
            Cw   -> Noise covariance matrix
            BMAT -> System matrix of Eq.(1)


    Harun Rashid 13-FEB-2003 (matlab version) 
                 15-SEP-2016 (python version)
    '''

# Check if 'time' is the first (longer) dimension

    vsh = v.shape
    if vsh[1] > vsh[0]:
       print("Time must be the first dimension!")

# Create "backshifted" augmented vector; exv = [B^1  B^2  B^3]*v

    lag = pord
    v = center(v)
    exv = extvecback(v,lag-1)                
    exv = exv[:-1,:]                       # Eliminate the last row

    v2 = v[lag:,:].copy()                  # Eliminate the p presample values
    n,m = v2.shape                         # n is same for both v and exv

    Cm1 = np.dot(v2.T,exv)/(n-1)           # Lag=-lag covariance matrix (m x mp) 
    C0  = np.dot(exv.T,exv)/(n-1)          # Lag= 0 covariance matrix (mp x mp)

    Amat = np.dot(Cm1,np.linalg.inv(C0))   # Coefficient matrix (m x mp)
    Cw = np.dot(v2.T,v2)/(n-1) - Amat.dot(C0).dot(Amat.T) # Eq. 7 of Penland and Sardeshmukh (1995;JC)

    if pord == 1:
        nlag=1
        Bmat = sp.linalg.logm(Amat)/nlag
    else:
        Bmat = []
        print('To compute B, A must be square!')

    return Amat,Cw,Bmat

def propagator(v, nlag=1):
# USAGE: Amat, Bmat = propagator(v, nlag)
# PROPAGATOR  Estimates the propagator and system matrix.
#
#    This PYTHON function estimates the propagator and system matrix, 
#      given a data array, v(nt,nx), each row of which represents a
#      "map" at a particular instance. The columns represent timeseries
#      anomalies at individual grid points, or of individual modes. The data
#      array is assumed to be the solution of vector linear equations
#      of the form:
#                     dv
#                    ----  = Bmat*v + F_wn        .............. (1)
#                     dt
#      or
#                     v(t+tau) = Amat*v(t) + F_wn(t+tau) ........(2)
#
#    INPUT:
#            v -> Input data array from which the matrices to be estimated
#            nlag -> Number of lags for lagged covariance matrix
#
#    OUTPUT:
#            Amat -> Propagator of Eq.(2)
#            BMAT -> System matrix of Eq.(1)
#
#
#  Harun Rashid 03-JAN-2003 (matlab version)
#               15-SEP-2016 (python version)

    if nlag < 1:
       print('nlag must not be < 1')
       return

    n,m = v.shape
    if n < m:
       print('n < m; looks like you have made a mistake!')

    #covlag = np.dot( v[nlag:,:].T,v[:n-nlag,:] )/(n-nlag)
    #cov0   = np.dot( v.T,v )/n
    covlag = np.dot( v[nlag:,:].T,v[:n-nlag,:] )/(n-1)
    cov0   = np.dot( v.T,v )/(n-1)

    Amat = np.dot(covlag, np.linalg.inv(cov0))
    Bmat = sp.linalg.logm(Amat)/nlag

    return Amat,Bmat

def varsim(coefs, intercept, sigma_u, steps=100, initvalues=None, seed=None):
    """
    Simulate simple VAR(p) process with known coefficients, intercept, white
    noise covariance, etc.

    Bug corrected on the statsmodels' original version (see below). 
    This function is similar to "arsim.m", but uses slightly different method.
    Comments and bug correction: Harun Rashid
    """
    if seed is not None:
        np.random.seed(seed=seed)
    from numpy.random import multivariate_normal as rmvnorm
    p, k, k = coefs.shape
    ugen = rmvnorm(np.zeros(len(sigma_u)), sigma_u, steps)
    result = np.zeros((steps, k))
    result[:p] = intercept
    result[p:] = intercept + ugen[p:]

    # add in AR terms
    for t in range(p, steps):
        ygen = result[t]
        for j in range(p):
            ygen += np.dot(coefs[j], result[t-j-1])
        result[t] = ygen          # this line is missing from the original version

    return result

def red_noise0(lag1,xvar,ntim=1000,ndis=1000):
    """
    Given the lag-1 autocorrelation and the variance of a timeseries, this function
    simulates the corresponding AR(1) or red noise process.

    This is a variant of 'arunisim' below, which does the same given the timeseries.

    Inputs:
       lag1 => lag-1 autocorrelation of a timeseries
       xvar => variance of the timeseries
       ntim => length of simulation
       ndis => spin-up length to be discarded

    07-OCT-2022
    """

    varnoise = (1-lag1**2)*xvar # variance of the "noise"
    ntim2 = ndis+ntim
    rvec = np.sqrt(varnoise)*np.random.randn(ntim2)

    x_rn0 = np.zeros(ntim2, "float")
    x_rn0[0] = rvec[0]
    for i in range(ntim2-1):
        x_rn0[i+1] = lag1*x_rn0[i] + rvec[i+1]

    return x_rn0[ndis:ntim2]

def red_noise(x0,ncopy=1,ndis=0,seed=None):
    """
    Given a time series, x0, this function computes the lag-1
    autocorrelation and the variance of the associated "noise".
    This information is then used to simulate an AR(1) process.

    This is similar to 'arunisim', but returns ncopies of red
    noise.

    03-AUG-2024
    """
    if seed is not None:
        np.random.seed(seed=seed)
    x = np.array(x0)
    ntim = len(x)
    lag1 = np.corrcoef(x[:-1],x[1:])[0,1] # lag-1 correlation
    stdnoise = np.sqrt((1-lag1**2)*np.var(x)) # Stdv of the "noise"
    ntim2 = ndis+ntim                         # ndis=0 is ok, as the initial values are from rvec
    rvec = np.random.default_rng().normal(scale=stdnoise,size=(ntim2,ncopy))

    x_rn0 = np.zeros(rvec.shape, "float")
    x_rn0[0] = rvec[0]
    for i in range(ntim2-1):
        x_rn0[i+1] = lag1*x_rn0[i] + rvec[i+1]

    return x_rn0[ndis:ntim2]

def arsim(lag1,xvar,ntim=1000,ndis=1000):
    """An alias of function red_noise0.
    """
    return red_noise0(lag1,xvar,ntim=ntim,ndis=ndis)

def arunisim(x,ndis=1000):
    """
    Given a time series, x, this function computes the lag-1
    autocorrelation and the variance of the associated "noise".
    This information is then used to simulate an AR(1) process.

    This is similar to my MATLAB function 'arunisim.m'.

    08-AUG-2007
    """
    ntim = len(x)
    lag1 = xcorr(x,nlag=1)[1]        # lag-1 correlation
    varnoise = (1-lag1**2)*np.var(x) # variance of the "noise"
    ntim2 = ndis+ntim
    rvec = np.sqrt(varnoise)*np.random.randn(ntim2)

    x_rn0 = np.zeros(ntim2, "float")
    x_rn0[0] = rvec[0]
    for i in range(ntim2-1):
        x_rn0[i+1] = lag1*x_rn0[i] + rvec[i+1]

    return x_rn0[ndis:ntim2]

def simpReg_slow (x, y):
    """
    Simple regression analysis between a 1-d or rank(y)-d time series (x, independant variable) and 
    an upto 3-d array (y, dependant variable). Time must be the first dimension in y.

    This function is slow for multi-dimensional arrays. Use simpReg() instead.
    """

    if isinstance(y,pd.DataFrame) or isinstance(y,pd.Series):
        return simpReg_df (x, y)

    shapex = x.shape
    shapey = y.shape
    rankx  = x.ndim
    ranky  = y.ndim
 
    if rankx not in [1,ranky] or shapex[0] != shapey[0]:
       print("x must be 1- or "+str(ranky)+"-d and/or time isn't the 1st dim in y")
       return

    # For numpy/xarray arrays; is there a faster way than looping?

    if rankx == 1 and ranky == 1:
       regC = sp.stats.linregress(x,y)[0]
    if ranky == 2:
       shape = y.shape[1]
       regC = np.zeros(shape)
       for i in range(shape):
          if rankx == 1:
             regC[i] = sp.stats.linregress(x,y[:,i])[0]
          elif rankx == ranky:
             regC[i] = sp.stats.linregress(x[:,i],y[:,i])[0]
    elif ranky == 3:
       shape = y.shape[1:]
       regC = np.zeros(shape)
       for j in range(shape[1]):
          for i in range(shape[0]):
             if rankx == 1:
                regC[i,j] = sp.stats.linregress(x,y[:,i,j])[0]
             elif rankx == ranky:
                regC[i,j] = sp.stats.linregress(x[:,i,j],y[:,i,j])[0]

    return regC

"""
   start_time = timeit.default_timer()   # no time advantage in this block of code
   x = np.array(x)
   y = np.array(y)
   if rank == 3:
      yt = np.swapaxes(y,0,2)
      shape = yt.shape[:-1]
      regC = np.zeros(shape)
      for i in range(shape[0]):
         for j in range(shape[1]):
            regC[i,j] = sp.stats.linregress(x,yt[i,j,:])[0]

   print(timeit.default_timer() - start_time)
"""

def simpReg (x0, y):
    """
    Simple regression analysis between a 1-d or rank(y)-d time series (x, independant variable) and 
    an upto n-d array (y, dependant variable). Time must be the first dimension in y.

    This function expects numpy/pandas/xarray arrays as inputs and is a lot faster (37 times) 
    than above. This function gives same result as NCL's regCoef function.
    """

    x = x0.copy()           # copy, as it may be modified below
    shapex = x.shape
    shapey = y.shape
    rankx  = x.ndim
    ranky  = y.ndim

    if rankx not in [1,ranky] or shapex[0] != shapey[0]:
       print("x must be 1- or "+str(ranky)+"-d and/or time isn't the 1st dim in y")
       return

    #if hasattr(x,'dims') and x.dims[0] != y.dims[0]:    # xarray
    #    #print(x0.dims[0]+' is renamed to '+y.dims[0])
    #    x = x.rename({x.dims[0]:y.dims[0]})
    #if rankx == 1 and hasattr(x0,'dims'):     # no need for xarray
    #    x = x.expand_dims(dim={'y':1},axis=1)
    if rankx == 1 and hasattr(x0,'dims'):     # xarray -> np.array
        x = x.values

    xp = x - x.mean(axis=0)
    yp = y - y.mean(axis=0)
    if isinstance(xp,np.ndarray) or isinstance(yp,np.ndarray):
       if rankx == 1:
          sl = list(shapex)
          dm = [sl.append(1) for n in range(ranky-1)]
          xp.shape = sl
    if isinstance(y,pd.DataFrame):
       numerator = yp.mul(xp,axis=0).sum(axis=0)
       denominat = xp.mul(xp,axis=0).sum(axis=0)
    else:                                        # numpy/xarray
       numerator = (xp*yp).sum(axis=0)
       denominat = (xp*xp).sum(axis=0)
    return numerator/denominat

def simpReg1 (x, y):
    """
    Simple regression analysis between a 1-d time series (x, independant variable) and 
    an upto n-d array (y, dependant variable). Time must be the first dimension in y.

    This function expects numpy/pandas/xarray arrays as inputs (not checked) and is a lot faster (62
    times) than simpReg_slow. This function gives same result as NCL's regCoef function.
    """

    shapex = x.shape
    shapey = y.shape
    rankx  = x.ndim
    ranky  = y.ndim

    if rankx not in [1] and shapex[0] != shapey[0]:
       print("x must be 1-d and/or time isn't the 1st dim in y")
       return

    xp = x - x.mean(axis=0)
    yp = y - y.mean(axis=0)
    if isinstance(xp,np.ndarray) or isinstance(yp,np.ndarray):
       numerator = tas.values.T.dot(ts1.values).T
    else:
       numerator = xp.dot(yp)
    denominat = xp.dot(xp)
    return numerator/denominat

def simpReg_df (x, y):
    """
    Simple regression analysis between a 1-d or rank(y)-d pd instance (x, independant
    variable) and 2-d pandas.DataFrame (y, dependant variable). 
    """

    if len(x.shape) == 1:
       if isinstance(y,pd.DataFrame):
          regD = y.apply(lambda y1: np.polyfit(x,y1,1),axis=0).T
          regD.columns = ['RegCoeff','Intercept']
          return regD
       elif len(y.shape) == 1:
          regD = np.polyfit(x,y,1)
          return pd.Series(regD,index=['RegCoeff','Intercept'])
       
    #if isinstance(x,pd.Series):
    #   p = np.polyfit(x, y, 1)
    #   if isinstance(y,pd.Series):
    #      return pd.Series(p,index=['RegCoeff','Intercept'])
    #   elif isinstance(y,pd.DataFrame):
    #      return pd.DataFrame(p,index=['RegCoeff','Intercept'],columns=y.columns).T
    #elif isinstance(x,pd.DataFrame) and isinstance(y,pd.DataFrame):
    if isinstance(x,pd.DataFrame) and isinstance(y,pd.DataFrame):
       if x.shape == y.shape:
          p = []
          p.extend([np.polyfit(x.iloc[:,i], y.iloc[:,i], 1) for i in range(y.shape[1])])
          #for i,col in enumerate(y.columns):                      # same as above
          #   p.append(np.polyfit(x.iloc[:,i], y[col], 1))
          return pd.DataFrame(p,columns=['RegCoeff','Intercept'],index=y.columns)
       else:
          regD = dict()
          for i,col in enumerate(x.columns):
             p = np.polyfit(x[col], y, 1)
             regD[col] = pd.DataFrame(p,index=['RegCoeff','Intercept'],columns=y.columns).T
          return regD
    else:
       print('x and y must be pd.Series and/or pd.DataFrame')
       return

def simpRegCorr (x0, y0, corr=False, axis=0):
    """
    Regress y0 on x0. Calculates one-point regression/correlation maps. 
    (Modified from https://currents.soest.hawaii.edu/ocn_data_analysis/_static/regression.html).

    x0 is a 1-D or n-D array with n points.
    y0 is at least 1-D or n-D, with n points along the dimension
    specified by axis.

    Returns (b1 or r), where b1 is the slope and r is the correlation
    coefficient.

    This function gives the same results as simpReg and simpCorr, but at least 2 times faster 
    than those. But simpReg and simpCorr work for x0 and y0 both being multidimensional arrays.

    No missing values are allowed. Use this function for data with no missing values. 
    """

    if x0.ndim > 1 and x0.ndim != y0.ndim:
        print("x must be 1-d or x.ndim == y.ndim!")
        return

    # Allow masked arrays and ordinary arrays, and remove the means.
    x = np.asanyarray(x0)
    x -= x.mean()
    y = np.asanyarray(y0)
    y -= y.mean(axis=axis, keepdims=True)
 
    if x.ndim == 1 and y.ndim > 1:   
        # Black magic to accomodate any dimensionality of y:
        bc = tuple([slice(None) if i == axis else np.newaxis 
                   for i in range(y.ndim)])
        Sxy = (x[bc] * y).sum(axis=axis)
    else:                            # x.ndim == y.ndim
        Sxy = (x*y).sum(axis=axis)
    
    # Note that we need only sums of squares and products.
    Sxx = (x**2).sum(axis=axis)

    if corr:
        Syy = (y**2).sum(axis=axis)
        r = Sxy / np.ma.sqrt(Sxx * Syy)
    else:
        r = Sxy / Sxx      # refCoeff

    if hasattr(y0,'dims'):        # xarray
        import xarray as xr
        da = y0[0]
        #r = xr.DataArray(r, coords=da.coords, dims=da.dims, attrs=da.attrs)
        r = xr.DataArray(r, coords=da.coords, dims=da.dims)
    elif isinstance(y0,pd.DataFrame):
        r  = pd.Series(r, y0.columns)

    return r

def simpCorr(x, y):
    """
    Simple correlation coefficient between a 1-d or rank(y)-d time series (x, independant variable) and 
    an upto 3-d array (y, dependant variable). Time must be the first dimension in y.
    """

    x = x/x.std(axis=0)
    y = y/y.std(axis=0)
    corr = simpReg (x, y)

    if hasattr(corr,'RegCoeff'):
        return corr['RegCoeff'].clip(-1,1)
    else:
        return corr.clip(-1,1)

def lagCorr (x0, y0, nlag):
    """
    Simple lag-correlation analysis between a 1-d or rank(y)-d time series (x) and an upto n-d array (y).
    Time must be the first dimension in y.

    This function expects numpy/pandas/xarray arrays as inputs. This is in general fast because of simpReg.

    This is slightly slower than crosscorr(), but should work for numpy/pandas/xarray fields. 
    This is same as lagCorr1_or (from numerical and speed perspectives).
    """
    import xarray as xr

    x = np.array(x0)  # This is needed for simpReg() to give correct
    y = np.array(y0)  # results for non-zero lags

    regP = []
    regN = []

    lagh = range(1,nlag+1)
    #regC = np.zeros(2*nlag+1)
    reg0 = simpCorr(x,y)
    for lg in lagh:
        regP.append(simpCorr(x[:-lg],y[lg:]))
        regN.append(simpCorr(x[lg:],y[:-lg]))

    lags = np.arange(-nlag,nlag+1,1)
    corrC = np.asarray([regN[::-1]+[reg0]+regP]).squeeze()
    if len(corrC.shape) == 1:
       corrC = pd.Series(corrC,index=lags)
    #elif isinstance(y0,pd.DataFrame):
    elif len(corrC.shape) == 2:
        corrC = pd.DataFrame(corrC,index=lags)
        if hasattr(y0,'columns'):
            corrC.columns = y0.columns
    elif hasattr(y0,'dims'):
        dims = ['lag']+list(y0.dims[1:])
        coords = {'lag':lags}
        coords.update({c:y0.coords[c] for c in dims[1:]})
        corrC = xr.DataArray(corrC, dims=dims, coords=coords)
             
    return corrC

def lagCorr_xr (da1, da2, time_dim='time', nlag=0):
    """
    Computes the lag correlation between two xarray DataArrays. Allows for missing
    values.

    Args:
        da1 (xr.DataArray): The first DataArray (1- or n-dimensional)
        da2 (xr.DataArray): The second DataArray (1- or n-dimensional)
        time_dim (str): The name of the time dimension
        lag (int): The lag in units of the time dimension. A positive lag
                   means da2 lags da1 (da2 is shifted forward in time).

    Returns:
        xr.DataArray: A DataArray containing the lag correlations.
    """

    if not isinstance(da1,xr.DataArray) or not isinstance(da2,xr.DataArray):
        print('Both input arrays must be an xr.DataArray!')
        print('For 1- or 2-d numpy, pandas and xarray , use: crosscorr')
        print('For 1- or n-d numpy, pandas and xarray , use: lagCorr, lagRegCorr (no missVals)')
        return

    lags = range(-nlag,nlag+1,1)
    corr = []
    for lag in lags:
        if lag > 0:
            # Shift da2 forward in time relative to da1
            da1_shifted = da1
            da2_shifted = da2.shift({time_dim: -lag})
        elif lag < 0:
            # Shift da1 forward in time relative to da2
            da1_shifted = da1.shift({time_dim: lag})
            da2_shifted = da2
        else:
            da1_shifted = da1
            da2_shifted = da2

        # xarray.corr handles NaN values by default, excluding them pairwise
        corr.append(xr.corr(da1_shifted, da2_shifted, dim=time_dim))

    if nlag == 0:
        return corr[0]
    else:
        correlation = xr.concat(corr, dim='lags')
        correlation['lags'] = lags
        return correlation

def lagReg (x0, y0, nlag):
    """
    Simple lag-regression analysis between a 1-d or rank(y)-d time series (x, independant variable)  
    and an upto n-d array (y, dependant variable). Time must be the first dimension in y.

    This function expects numpy/pandas/xarray arrays as inputs. This is more than 4 times faster 
    than lagReg_df for pandas objects, and is in general fast because of simpReg. 
    """
    import xarray as xr

    x = np.array(x0)  # This is needed for simpReg() to give correct
    y = np.array(y0)  # results for non-zero lags

    regP = []
    regN = []

    lagh = range(1,nlag+1)
    #regC = np.zeros(2*nlag+1)
    reg0 = simpReg(x,y)
    for lg in lagh:
       regP.append(simpReg(x[:-lg],y[lg:]))
       regN.append(simpReg(x[lg:],y[:-lg]))

    lags = np.arange(-nlag,nlag+1,1)
    if isinstance(x0,xr.DataArray) or isinstance(y0,xr.DataArray):
       regC = xr.DataArray(np.concatenate([regN[::-1]+[reg0]+regP]), coords={'lag':lags,'lat':x0.lat,'lon':x0.lon})
    else:
       regC = np.asarray(regN[::-1]+[reg0]+regP) # numpy/pandas objects
       regC = pd.DataFrame(regC,index=lags)
       if hasattr(x0,'columns'): regC.columns = x0.columns

    return regC

def lagReg_df (x, y, nlag):
    """
    Simple lag regression analysis between a 1-d time series (x, independant variable)
    and 1-d array (y, dependant variable). Time must be the first dimension in y.

    Note: This function is obsolete now; use lagReg() for pandas Series and DataFrames. 
    """

    if isinstance(x,pd.Series):
        if isinstance(y,pd.Series):
            return lagReg_sr (x, y, nlag)
        elif isinstance(y,pd.DataFrame):
            return y.apply(lambda z: lagReg_sr(x,z,nlag))
    elif isinstance(x,pd.DataFrame) and y.shape == x.shape:
        regC = {}
        for i,col in enumerate(y.columns):
            regC[col] = lagReg_sr (x.iloc[:,i], y[col], nlag)
        return regC
    else:
        print('Incompatible arrays!')
        return    

def lagReg_sr (x, y, nlag):
    """
    Simple lag regression analysis between a 1-d time series (x, independant variable)
    and 1-d array (y, dependant variable). Time must be the first dimension in y.
 
    Note: This function is obsolete now; use lagReg() for pandas Series and DataFrames.
    """

    if len(x.shape) == len(y.shape) == 1:
    #if isinstance(x,pd.Series) and isinstance(y,pd.Series):
        regC = lagReg(x, y, nlag)
        return regC
    else:
        print('x and y must be 1-d array/series!')
        return

def regResid_np (x0, y0):
    """
    Remove the effect of x from y by simple regression.

    Simple regression analysis between a 1-d or rank(y)-d time series (x, independant variable) and 
    an upto 3-d array (y, dependant variable). Time must be the first dimension in y. Accepts
    numpy inputs only. Call regResid() for numpy/pandas/xarray inputs

    This function allows for removing a first-order fit (i.e., nord=1), as opposed to
    regResid_nord further up which works for nord>=1. But this function is a lot faster than 
    regResid_nord (for nord=1).

    This is the fastest call to regResid (implemented below)
        df_out = pd.DataFrame(ms.regResid(x.values,y.values), columns=y.columns, index=y.index)
    """

    #idx = np.isfinite(x0) & np.isfinite(y0[:,0]) # presents multiple problems
    #x = np.array(x0[idx])                     # copy, as it may be modified below
    #y = np.array(y0[idx])
    x = np.array(x0)                     # copy, as it may be modified below
    y = np.array(y0)
    shapex = x.shape
    shapey = y.shape
    rankx  = x.ndim
    ranky  = y.ndim
 
    if rankx not in [1,ranky] or shapex[0] != shapey[0]:
       print("x must be 1- or "+str(ranky)+"-d and/or time isn't the 1st dim in y")
       return

    #For numpy arrays

    regc = simpReg(x,y)
    intc = y.mean(axis=0) - regc*x.mean(axis=0)
    #print(regc,intc)
    if isinstance(x,np.ndarray) or isinstance(y,np.ndarray):
       if rankx == 1:
          sl = list(shapex)
          dm = [sl.append(1) for n in range(ranky-1)]
          x.shape = sl
       return y - x*regc - intc  # = y - yave - regc*(x - xave)
    else:
       print("This function is for numpy arrays, intended for internal use only.")
       print("Call ms.regResid() for numpy/pandas/xarray arrays.")
       return
"""
    elif isinstance(y,pd.DataFrame):
       xv = x.values
       if rankx == 1:
          sl = list(shapex)
          dm = [sl.append(1) for n in range(ranky-1)]
          xv.shape = sl
       yprime = y.values - xv*regc.values - intc.values  # = y - yave - regc*(x - xave)
       yprime = pd.DataFrame(yprime,columns=y.columns,index=y.index)
    else:                          # assumes xarray
       yprime = y - x*regc - intc  # = y - yave - regc*(x - xave)
    return yprime
"""

def regResid (x, y):
    """
    Remove the effect of x from y by simple regression analysis between a 1-d or rank(y)-d 
    time series (x, independant variable) and an upto 3-d array (y, dependant variable). Time
    must be the first dimension in y. Accepts numpy/pandas/xarray inputs.

    This function allows for removing a first-order fit (i.e., nord=1), as opposed to
    regResid_nord further up which works for nord>=1. But this function is a lot faster than 
    regResid_nord (for nord=1).

    This is the newest version with faster calculations for Series-DataFrame inputs.
    The fastest call is in terms of numpy inputs:
        df_out = pd.DataFrame(ms.regResid(x.values,y.values), columns=y.columns, index=y.index)
    The numpy method is implemented here.
    """
    if isinstance(x,np.ndarray) or isinstance(y,np.ndarray):
        return regResid_np (x, y)
    elif isinstance(y,pd.DataFrame):
        return pd.DataFrame(regResid_np(x.values,y.values), columns=y.columns, index=y.index)
    elif isinstance(y,pd.Series):
        return pd.Series(regResid_np(x.values,y.values), index=y.index)
    else:
        import xarray as xr
        return xr.DataArray(regResid_np(x.values,y.values), dims = y.dims, coords = y.coords)

def run_mean(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / N

def forecast1 (params, x, pord, fclen):
    """Calculates autoregressive model forecasts, given the AR parameters (params),
    intitial values (x), and forecast length (fclen). A use of this function may be 
    found in ar_forecast() below.
    See https://stackoverflow.com/questions/63428622/how-to-forecast-time-series-using-autoreg-in-python

    Proces all start times at once:
    df_temp = pd.DataFrame(ms.extvec(datf['Nino3.4'],pord-1),index=datf.index[pord-1:])
    p1 = params[1:].copy()
    p1.index = df_temp.columns
    dict_pred = {}
    for l in range(fclen):
        pred = params[0] + p1.dot(df_temp.T)
        #pred = pred.shift() # These are forecasts, so shift the dates
        #pred = params[0] + np.sum(params[1:].values*df_temp.values,axis=1)
        df_temp=df_temp.shift(-1,axis=1)
        df_temp[pord-1] = pred.values
        dict_pred['L'+str(l+1)] = pred

    df_pred = pd.DataFrame(dict_pred)

    """
    preds = []
    for t in range(fclen):
        pred = params[0] + np.sum(params[1:]*x[::-1])
        x[:pord-1], x[pord-1] = x[-(pord-1):], pred
        preds.append(pred)

    return np.array(preds)

def forecast (params, datf, pord, fclen):
    """Calculates autoregressive model forecasts, given the AR parameters (params),
    intitial values (x), and forecast length (fclen). A use of this function may be 
    found in ar_forecast() below.
    See https://stackoverflow.com/questions/63428622/how-to-forecast-time-series-using-autoreg-in-python

    This function proceses all start times at once.
    """

    if len(datf.shape) != 1:
      print("Input data must be 1-d; call var_forecast() for 2-d data")
      return

    #df_temp = pd.DataFrame(extvec(datf,pord-1),index=datf.index[pord-1:])
    df_temp = pd.DataFrame(extvecback(datf[:-fclen+1],pord-1),index=datf.index[pord-1:-fclen+1])
    p1 = params[1:].copy()
    p1.index = df_temp.columns
    dict_pred = {}
    for l in range(fclen):
        pred = params[0] + p1.dot(df_temp.T)
        df_temp=df_temp.shift(1,axis=1)
        df_temp[0] = pred.values
        dict_pred['L'+str(l+1)] = pred

    df_pred = pd.DataFrame(dict_pred)
    return df_pred.shift().dropna()
    #return df_pred.shift().dropna()[:-fclen+1]

def ar_forecast(data,datf,pord,fcmonth=15,fcintv=1):
   '''Given the training dataset (data) and the verification dataset (datf),
   fit a AR model of order "pord", make forecasts and calculate forecast
   statistics: anom_corr, rmse and explained variance. 

   Inputs:
      data => training data[ntime], a pd.Series object 
      datf => training datf[ntime], a pd.Series object
      pord => order of the AR model to be fitted
      fcmonth => forecast length [default = 15 mons]
      fcintv => fc starts every fcintv interval [default = 1 mons]                                      # 
   Lengths of the two data arrays can differ. 

   Outputs:
      Anomaly correlations, RMSE, and explained variances by an AR(p) model

   06-FEB-2023 Harun Rashid
   '''

   from statsmodels.tsa.ar_model import AutoReg

   if len(data.shape) != 1:
      print("Input data must be 1-d; call var_forecast() for 2-d inputs")
      return

   index = datf.index
   #datf = datf.values

   result = AutoReg(data, lags=pord).fit()

   totVar = data.var()
   expVar = 1 - result.resid.var()/totVar

   #ntim = datf.shape[0]
   #fc_starts = range(1,ntim,fcintv)
   #nstarts = len(fc_starts)

   #fc_sst = np.zeros([nstarts+1,fcmonth])
   #fc_sst[:] = np.nan
   #for ns in fc_starts[pord-1:]:
   #    x = datf[ns-pord:ns].copy().values
   #    fc_sst[ns,:] = forecast1(result.params, x, pord, fcmonth)

   columns = ['L'+str(i+1) for i in range(fcmonth)]
   ind_short = index[pord:-fcmonth+1]
   enso = pd.DataFrame(extvec(datf[pord:],fcmonth-1),columns=columns,index=ind_short)
   #fct  = pd.DataFrame(fc_sst[pord:-fcmonth+1,:],columns=columns,index=ind_short)
   fct  = forecast(result.params,datf,pord,fcmonth)
   ano_corr = enso.corrwith(fct)
   temp = ((enso-fct)**2).mean()**0.5
   rmse = temp/enso['L1'].std()

   return ano_corr, rmse, expVar

def var_forecast(data,datf,pord,npcs=1,fcmonth=15,fcintv=1):
   '''Given the training dataset (data) and the verification dataset (datf),
   fit a VAR model of order "pord", make forecasts and calculate forecast
   statistics: anom_corr, rmse and explained variance. 

   Inputs:
      data => training data[ntime,nmodes], a pd.DataFrame object (nmodes >= 2)
      datf => training datf[ntime,nmodes], a pd.DataFrame object
      pord => order of the VAR model to be fitted
      npcs => number of timeseries for which forecast stats to be calculated [default=1]
      fcmonth => forecast length [default = 15 mons]
      fcintv => fc starts every fcintv interval [default = 1 mons]                                      # 
   Lengths of the two data arrays can differ, but nmodes must be the same. 

   Outputs:
      Anomaly correlations, RMSE, and explained variances by VAR(p) model

   26-APR-2018 Harun Rashid
   '''

   from statsmodels.tsa.api import VAR


   if len(data.shape) != 2:
      print("Input data must be 2-d; call ar_forecast() for 1-d inputs")
      return

   index = datf.index
   datf = datf.values

   model = VAR(data)
   result = model.fit(pord)                                   # pord = 2 explains 98% of total variance

   totVar = data.var()
   expVar = 1 - result.resid.var()/totVar

   ntim,nmode = datf.shape
   fc_starts = range(1,ntim,fcintv)
   nstarts = len(fc_starts)

   fc_sst = np.zeros([nstarts+1,fcmonth,nmode])
   fc_sst[:] = np.nan
   for ns in fc_starts[pord-1:]:
      fc_sst[ns,:,:] = result.forecast(datf[ns-pord:ns,:], fcmonth)

   columns = ['L'+str(i+1) for i in range(fcmonth)]
   ind_short = index[pord:-fcmonth+1]
   for m in range(npcs):
      enso = pd.DataFrame(extvec(datf[pord:,m],fcmonth-1),columns=columns,index=ind_short)
      fct  = pd.DataFrame(fc_sst[pord:-fcmonth+1,:,m],columns=columns,index=ind_short)
      if m == 0:
         ano_corr = enso.corrwith(fct)
         temp = ((enso-fct)**2).mean()**0.5
         rmse = temp/enso['L1'].std()
      else:
         ano_corr = pd.concat([ano_corr,enso.corrwith(fct)],axis=1)
         temp = ((enso-fct)**2).mean()**0.5
         rmse = pd.concat([rmse,temp/enso['L1'].std()],axis=1)

   return ano_corr, rmse, expVar

def spectrum1(h, dt=1): 
   """
   First cut at spectral estimation: very crude.
   Returns frequencies, power spectrum, and
   power spectral density.
   Only positive frequencies between (and not including
   the Nyquist) are output.
   """
   nt = len(h)
   npositive = nt//2
   pslice = slice(1, npositive)
   freqs = np.fft.fftfreq(nt, d=dt)[pslice]
   ft = np.fft.fft(h)[pslice]
   psraw = np.abs(ft) ** 2
   # Double to account for the energy in the negative frequencies. 
   psraw *= 2
   # Normalization for Power Spectrum
   psraw /= nt**2
   # Convert PS to Power Spectral Density
   psdraw = psraw*dt*nt # nt*dt is record length
   return freqs, psraw, psdraw

def spectrum2(h, dt=1, nsmooth=11, window='hanning'): 
   """
   Add smoothing to the raw periodogram.
   Chop off the ends to avoid end effects.
   """
 
   freqs, ps, psd = spectrum1(h, dt=dt)
   weights = get_weights (nsmooth, window=window)
   #weights = np.ones(nsmooth, dtype=float) / nsmooth 

   nh = nsmooth//2
   xb = ps[:nh]   # First k elements
   xt = ps[-nh:]  # Last k elements
   ps = np.concatenate((xb[::-1], ps, xt[::-1])) # reflective boundaries
   yb = psd[:nh]   # First k elements
   yt = psd[-nh:]  # Last k elements
   psd = np.concatenate((yb[::-1], psd, yt[::-1]))

   cmode = 'valid'
   ps_s = np.convolve(ps, weights, mode=cmode)
   psd_s = np.convolve(psd, weights, mode=cmode)
   #nh = nsmooth//2
   #ps1 = np.full(ps.shape, np.nan)  # no longer needed, due to applying reflective BC
   #psd1 = np.full(psd.shape, np.nan)
   #ps1[nh:-nh] = ps_s
   #psd1[nh:-nh] = psd_s
   return freqs, ps_s, psd_s

def spectrum4(h, dt=1, dtrend=1, nsmooth=5):
    """
    Detrend and apply a quadratic window.
    """
    n = len(h)

    if dtrend in [1,2]:
       h_detrended = detrend(h,dtrend)
    else:
       h_detrended = h

    winweights = quadwin(n) # alternative to taper, not window
    h_win = h_detrended * winweights
    
    freqs, ps, psd = spectrum2(h_win, dt=dt, nsmooth=nsmooth, window='flat')
    
    # Compensate for the energy suppressed by the window.
    psd *= n / (winweights**2).sum()
    ps *= n**2 / winweights.sum()**2
    
    return freqs, ps, psd

def specx (h, dt=1, dtrend=1, nsmooth=11, window='hanning'): 
   """
   This should give the same result as NCL's specx_anal function. Apply a
   tapering window and normalise as in specx_anal.

   Refs:
       https://currents.soest.hawaii.edu/ocn_data_analysis/_static/Spectrum.html
       https://www.ncl.ucar.edu/Document/Functions/Built-in/specx_anal.shtml (example 4) 
   """

   nt = len(h)
   if dtrend in [1,2]:
      h_detrended = detrend(h,dtrend)
   else:
      h_detrended = h
   winweights = taper(nt,0.1)
   h_win = h_detrended * winweights
   varh = h_detrended.var()

   freqs, ps, psd = spectrum2(h_win, dt=dt, nsmooth=nsmooth, window=window)
   # Compensate for the energy suppressed by the window.
   psd *= nt / (winweights**2).sum()  # original normalisation as above
   ps[0] = 0.5*ps[0]
   #ps[-1] = 0.5*ps[-1]   # not needed, as ps doesn't include NyqFreq
   df = (freqs[1]-freqs[0])*dt 
   #print(len(varh*ps))
   #print(len(np.nansum(ps*df)))      
   ps = varh*ps/np.nansum(ps*df)     # NCL normalisation (roughly)

   return freqs, ps, psd

def specx_ci (ps,nsmooth,pval=0.05,window='hanning'):
   """
   Compute the confidence interval for spectrum estimated in specx. May be plotted
   as:
   fig, ax = plt.subplots()
   ax.semilogy(freqs1, psd1, 'b', alpha=0.5)
   ax.semilogy(freqs1a, psd1a, 'r', alpha=0.5)

   ax.plot([conf_x, conf_x], conf, color='k', lw=1.5)
   ax.plot(conf_x, conf_y0, color='k', linestyle='none', 
        marker='_', ms=8, mew=2)

   Ref:
       https://currents.soest.hawaii.edu/ocn_data_analysis/_static/Spectrum.html
   Ref for DOFs:
       http://pordlabs.ucsd.edu/sgille/sioc221a_f17/lecture16_notes.pdf 
   """

   #import scipy.stats as ss

   df = 2*nsmooth # DOF for nsmooth-point boxcar smoother
   if window == 'hanning':
       df = df*8/3    # DOF Hanning window (Ref: Table 1 of the 2nd Ref above)
   elif window == 'hamming':
       df = df*2.5164 # DOF Hamming window 
   elif window == 'bartlett':
       df = df*3.0
   elif window == 'parzen':
       df = df*3.708614

   ci = [pval/2,1-pval/2]
   conf = ps[:,np.newaxis] * df / scipy.stats.chi2.ppf(ci, df)

   return conf

def lanczos_lp(window, cutoff):
    """
       Calculate weights for a low pass Lanczos filter.

    Args:

    window: int
        The length of the filter window.

    cutoff: float
        The cutoff frequency in inverse time steps.

    Usage:
    # construct a 7-year (84-month) low pass filter:
    wgts84 = low_pass_weights(window, 1. / 84.)

    # apply the filters using the rolling_window method with the weights
    # keyword argument
    soi84 =  soi.rolling_window('time',
                                iris.analysis.MEAN,
                                len(wgts84),
    butter_bandpass_filter                            weights=wgts84)

    Source: https://scitools.org.uk/iris/docs/v1.2/examples/graphics/SOI_filtering.html
    """
    order = ((window - 1) // 2 ) + 1
    nwts = 2 * order + 1
    w = np.zeros([nwts])
    n = nwts // 2
    w[n] = 2 * cutoff
    k = np.arange(1., n)
    sigma = np.sin(np.pi * k / n) * n / (np.pi * k)
    firstfactor = np.sin(2. * np.pi * cutoff * k) / (np.pi * k)
    w[n-1:0:-1] = firstfactor * sigma
    w[n+1:-1] = firstfactor * sigma
    return w[1:-1]

def filter_lanczos_sr (y, window, cutoff):
    """
       Lanczos low-pass filter. 
    Inputs:
       y = timeseries to be filtered (1-D)
       window = window length or number of weights
       cutoff = low-pass cutoff frequency
    """
    import xarray as xr

    weights = lanczos_lp(window,cutoff)

    if type(y) == xr.DataArray or type(y) == np.ndarray:
        weight = xr.DataArray(weights, dims=['window'])
        if type(y) == np.ndarray:
            y = xr.DataArray(y, dims=['time'],coords={'time':np.arange(len(y))})
        #if y.dims[0] != 'time': y = y.rename({y.dims[0]:'time'})
        return y.rolling(time=len(weight), center=True).construct('window').dot(weight)
    elif type(y) == pd.DataFrame or type(y) == pd.Series:
        return y.rolling(len(weights), center=True).apply(lambda x: np.sum(weights*x))
    else:
        print('Inputs must be pd.DataFrames or xr.DataArray (1d) or np.ndarray')
        return

def filter_lanczos (y, window, cutoff):
    """
       Lanczos low-pass filter. 
    Inputs:
       y = timeseries to be filtered (1-/2-D)
       window = window length or number of weights
       cutoff = low-pass cutoff frequency
    """

    if hasattr(y,'dims') and y.dims[0] != 'time': y = y.rename({y.dims[0]:'time'})

    if type(y) == pd.DataFrame:
        return y.apply(lambda x: filter_lanczos_sr(x, window, cutoff))
    elif y.ndim == 1:
        return filter_lanczos_sr(y, window, cutoff)
    elif y.ndim == 2:
        nt,nx = y.shape
        yp = y.copy()
        for i in range(nx):
            yp[:,i] = filter_lanczos_sr(yp[:,i], window, cutoff)
        return yp
    elif y.ndim == 3 and type(y) != np.ndarray:
        nt,ny,nx = y.shape
        yp = y.copy()
        for j in range(ny):
            for i in range(nx):
                #print(j,i)
                yp[:,j,i] = filter_lanczos_sr(yp[:,j,i], window, cutoff)
        return yp
        """
        dims = y.dims
        yp = y.transpose(dims[1],dims[2],dims[0])
        #yp = np.zeros_like(y)
        for j in range(ny):
            for i in range(nx):
                #print(j,i)
                yp[j,i,:] = filter_lanczos_sr(yp[j,i,:], window, cutoff)
        return yp.transpose(dims[0],dims[1],dims[2])
        """
    else:
        print('Inputs must be pd.DataFrames or xr.DataArray or np.ndarray (ndim<=3')
        return

def filter_temp (y, winlen, cutoff):
    """
    Lanczos low-pass filter.
 
    Inputs:
       y = timeseries of pd.DataFrames or xr.DataArray or np.ndarray (1-3 D)
       winlen = window length or number of weights
       cutoff = low-pass cutoff frequency

    This is a lot faster than filter_lanczos above.
    """
    from scipy.signal import fftconvolve
    import xarray as xr

    weights = lanczos_lp(winlen,cutoff)
    w = weights/weights.sum()
    if y.ndim == 1:
        wt = w
    elif y.ndim == 2:
        wt = np.zeros((winlen,1))
        wt[:,0] = w
    elif y.ndim == 3:
        wt = np.zeros((winlen,1,1))
        wt[:,0,0] = w
    yp = fftconvolve(y.values,wt,mode='same')

    if isinstance(y,pd.DataFrame):
        return pd.DataFrame(yp,index=y.index,columns=y.columns)
    elif isinstance(y,xr.DataArray):
        return copy_varMeta(y,yp)
    else:
        return yp

def calculate_vif(X0):
    """
    Calculate variance inflation factor (VIF) to determine multi-colinearity
    of data matrix. If the VIF is greater than 5-10, multicolinearity  
    is likely present and the variable should be dropped. Ref:
             https://etav.github.io/python/vif_factor_python.html
             James et al. 2015: An Introduction to Statitical Learning. P. 99-102
    The number of colinear variables may be found by counting the VIF values>5:
      np.sum(vif>5)
    """
    from statsmodels.stats.outliers_influence import variance_inflation_factor    
    from statsmodels.tools.tools import add_constant

    X = add_constant(X0)
    cols = X.columns
    variables = np.arange(X.shape[1])
    c = X[cols[variables]].values
    vif = [variance_inflation_factor(c, ix) for ix in np.arange(c.shape[1])]
    return pd.Series(vif[1:],index=cols[1:])

def crosscorr(datax, datay, lag=10):
    """ Lag-N cross/auto correlation for each column of two/one dataframes. 
    Parameters
    ----------
    lag : int, default 10
    datax, datay : 1- or 2-D pandas.DataFrame/xarray.DataArray

    Returns
    ----------
    crosscorr : DataFrame
    """
    import xarray as xr

    if datax.shape[0] != datay.shape[0]:
       print('DataFrames/DataArrays must be of the same length')
       return

    if len(datax.shape) > 2 or len(datay.shape) > 2:
       print('DataFrames/DataArrays must be 1- or 2-D!')
       print('Use: lagCorr_xr (1 or n dim) or lagCorr (no missVals) instead')
       return
    elif isinstance(datax,pd.Series) and isinstance(datay,pd.Series):
       miss_val = datax.isnull().any() | datay.isnull().any()
       corr = lagCorr1(datax, datay, lag, miss_val)
       return corr
 
    if len(datax.shape) == 1:
       if type(datax)==xr.DataArray:
           datax = datax.to_series()
       datax = pd.concat([datax]*datay.shape[1],axis=1) # series to df by repeating column
       datax.columns = datay.columns
    elif  datax.shape[1] != datay.shape[1]: 
       print('datax must have either 1 or datay.shape[1] columns!')
       return

    corrd = {}
    if type(datax) == pd.DataFrame and type(datay) == pd.DataFrame:
       colx = datax.columns
       coly = datay.columns
    elif type(datax)==xr.DataArray and type(datay)==xr.DataArray:
       datax = datax.to_pandas()
       datay = datay.to_pandas()
       colx = datax.columns
       coly = datay.columns
    else:
       print('Inputs must be pd.DataFrames or xr.DataArray (2d)')
       return

    miss_vals = datax.isnull().any() | datay.isnull().any()
    for i,col in enumerate(colx):
       lcorr = lagCorr1(datax[col],datay.iloc[:,i],lag,miss_vals[col])
       corrd[col] = lcorr

    return pd.DataFrame(corrd)

def pearsonr_ci(x,y,alpha=0.05):
    ''' calculate Pearson correlation along with the confidence interval using scipy and numpy
    Parameters. 

    My note: Serial correlation is _not_ taken into account in calculating standard error (se)
    ----------
    x, y : iterable object such as a list or np.array
      Input for correlation calculation
    alpha : float
      Significance level. 0.05 by default
    Returns
    -------
    r : float
      Pearson's correlation coefficient
    pval : float
      The corresponding p value
    lo, hi : float
      The lower and upper bound of confidence intervals

    From: https://zhiyzuo.github.io/Pearson-Correlation-CI-in-Python/
    '''

    r, p = sp.stats.pearsonr(x,y)
    r_z = np.arctanh(r)
    se = 1/np.sqrt(x.size-3)
    z = sp.stats.norm.ppf(1-alpha/2)
    lo_z, hi_z = r_z-z*se, r_z+z*se
    lo, hi = np.tanh((lo_z, hi_z))
    return r, p, lo, hi

def bootstrap_correl0(x,y,ncopy=1000,ci=[0.025,0.975]):
    ''' Calculates bootstrap confidence intervals for corr(x,y).

    Difference from bootstrap_correl below:
        This function randomises x only, keeping y unchanged. This means the
        median or average corrCoeff is 0, and the confidence interval is now
        around 0 correlation.
   
    Inputs:
        x,y => input time series (1-D)
        ncopy => number of bootstrap samples (default=1000, minimum number)
        ci => desired confidence levels (default = 5%,95%, two tailed)
    Returns:
        corrC => corrCoeff(x,y)
        conf_interval => confidince interval values
        r_all => sorted corrCoeffs for all bootstrap samples (ncopy)
        std_err => standard error 
    '''

    if ncopy < 1000:
       print("Minimum bootstrap copies should be >= 1000")

    x = np.array(x)
    y = np.array(y)

    #ci1 = int(ci[0]*ncopy)
    #ci2 = int(ci[1]*ncopy)
    corrC = np.corrcoef(x,y)[0,1]
    idx = np.random.randint(len(x),size=(ncopy,len(x)))
    bx = x[idx]
    #by = y[idx]
    by = y[:,np.newaxis].repeat(ncopy,1).T
    mx = np.mean(bx,1)
    my = np.mean(by,1)
    sx = np.std(bx,1)
    sy = np.std(by,1)
    r_all = np.sort(np.sum( (bx - mx.repeat(len(x),0).reshape(bx.shape))* \
           (by - my.repeat(len(y),0).reshape(by.shape)), 1)/((len(x)-1)*sx*sy))
    #bootstrap confidence interval (NB! biased)
    conf_interval = (np.quantile(r_all,ci[0]),np.quantile(r_all,ci[1]))
    #conf_interval = (r_all[ci],r_all[ci2])
    #bootstrap standard error using Fisher's z-transform (NB! biased)
    std_err = np.tanh(np.std(np.arctanh(r_all))*(len(r_all)/(len(r_all)-1.0)))

    return (corrC, conf_interval, r_all, std_err)

def bootstrap_correl(x,y,ncopy=1000,ci=[0.025,0.975]):
    ''' Calculates bootstrap confidence intervals for corr(x,y).
    Inputs:
        x,y => input time series (1-D)
        ncopy => number of bootstrap samples (default=1000, minimum number)
        ci => desired confidence levels (default = 5%,95%, two tailed)
    Returns:
        corrC => corrCoeff(x,y)
        conf_interval => confidince interval values
        r_all => sorted corrCoeffs for all bootstrap samples (ncopy)
        std_err => standard error 
    '''

    if ncopy < 1000:
       print("Minimum bootstrap copies should be >= 1000")

    x = np.array(x)
    y = np.array(y)

    #ci1 = int(ci[0]*ncopy)
    #ci2 = int(ci[1]*ncopy)
    corrC = np.corrcoef(x,y)[0,1]
    idx = np.random.randint(len(x),size=(ncopy,len(x)))
    bx = x[idx]
    by = y[idx]
    mx = np.mean(bx,1)
    my = np.mean(by,1)
    sx = np.std(bx,1)
    sy = np.std(by,1)
    r_all = np.sort(np.sum( (bx - mx.repeat(len(x),0).reshape(bx.shape))* \
           (by - my.repeat(len(y),0).reshape(by.shape)), 1)/((len(x)-1)*sx*sy))
    #bootstrap confidence interval (NB! biased)
    conf_interval = (np.quantile(r_all,ci[0]),np.quantile(r_all,ci[1]))
    #conf_interval = (r_all[ci1],r_all[ci2])
    #bootstrap standard error using Fisher's z-transform (NB! biased)
    std_err = np.tanh(np.std(np.arctanh(r_all))*(len(r_all)/(len(r_all)-1.0)))

    return (corrC, conf_interval, r_all, std_err)

def bootstrap_rmse(x,y,ncopy=1000,ci=[0.025,0.975]):
    ''' Calculates bootstrap confidence intervals for rmse(x,y).
    Inputs:
        x,y => input time series (1-D)
        ncopy => number of bootstrap samples (default=1000, minimum number)
        ci => desired confidence levels (default = 5%,95%, two tailed)
    Returns:
        rmse => rmse(x,y)
        conf_interval => confidince interval values (two-tailed; should ci be one-tailed, as rmse is +ve?)
        r_all => sorted rmse for all bootstrap samples (ncopy)
        std_err => standard error 
    '''

    x = np.array(x)
    y = np.array(y)

    if ncopy < 1000:
       print("Minimum bootstrap copies should be >= 1000")

    ci1 = int(ci[0]*ncopy)
    ci2 = int(ci[1]*ncopy)
    rmse = np.sqrt(np.mean((x-y)**2))
    idx = np.random.randint(len(x),size=(ncopy,len(x)))
    bx = x[idx]
    by = y[idx]
    #mx = np.mean(bx,1)
    #my = np.mean(by,1)
    #sx = np.std(bx,1)
    #sy = np.std(by,1)
    r_all = np.sort(np.sqrt(np.mean((bx - by)**2,1)))
    #bootstrap confidence interval (NB! biased)
    conf_interval = (r_all[ci1],r_all[ci2])

    return (rmse, conf_interval, r_all)

def wgt_areaave0 (fld):
    ''' Calculates lat weighted area average for an xarray.DataArray object.
    Input 'fld' must be xarray.DataArray; for Numpy arrays, use np.average().
    No NaNs are allowed.
        Can't handle (time-dependent?) missing values (e.g. ERSST). Use for
    data with no missing values only. 
    '''    

    if not hasattr(fld,'dims') or not hasattr(fld,'coords'):
       print("Input data must have 'dims' and 'coords' attributes.")
       print("Possibly not a xarray.DataArray.")
       sys.exit()

    dims = fld.dims
    if 'lat' in dims:
       latn = 'lat'
       lati = dims.index('lat')
    elif 'latitude' in dims:
       latn = 'latitude'
       lati = dims.index('latitude')
    else:
       print('No valid latitude name!')
       sys.exit()

    lat_wgt = np.cos(np.deg2rad(fld.coords[latn]))
    lat_wgt = lat_wgt/lat_wgt.sum()
    fld_ave = np.average(fld,axis=lati,weights=lat_wgt).mean(axis=-1) # same as NCL's wgt_areaave()

    return fld_ave

def wgt_areaave1 (fld):
    ''' Calculates cos(lat) weighted area average for an xarray.DataArray object.
    Input 'fld' must be xarray.DataArray; for Numpy arrays, use np.average().
       
        Properly deals with (time-dependent?) missing values (e.g. ERSST)

    Note: This function was verified with wgt_areaave below, but this function is
        1.44 times faster (but slower for large arrays).
    '''    

    if not hasattr(fld,'dims') or not hasattr(fld,'coords'):
       print("Input data must have 'dims' and 'coords' attributes.")
       print("Possibly not a xarray.DataArray.")
       sys.exit()

    dims = fld.dims
    if 'lat' in dims:
       latn = 'lat'
       lati = dims.index('lat')
    elif 'latitude' in dims:
       latn = 'latitude'
       lati = dims.index('latitude')
    else:
       print('No valid latitude name!')
       return

    if lati == 0:
       lat_wgt = fld[:,0].copy()      # needed for correct broadcasting below
    elif lati == 1:
       lat_wgt = fld[0,:,0].copy()      # needed for correct broadcasting below
    else:
       print('Only 2-d & 3-d fields are valid!')
       return

    lat_wgt[:] = np.cos(np.deg2rad(fld.coords[latn]))
    fldg = lat_wgt*fld
    latw3 = fldg/fld          # get 3-d weights
    #fld_ave = fldg.sum(dims[-2:],skipna=True)/latw3.sum(dims[-2:],skipna=True)
    fld_ave = fldg.sum(dims[-2:])/latw3.sum(dims[-2:])

    '''
    fldz = fld.mean(dims[-1])   # not correct
    lat_wgt = fldz[0,:]
    lat_wgt[:] = np.cos(np.deg2rad(fld.coords[latn]))
    fldg = lat_wgt*fldz
    latw2 = fldg/fldz
    fld_ave = fldg.sum(latn)/latw2.sum(latn)
    '''
    '''
    import xarray as xr      # as the active code above, but perhaps less efficient

    lat_wgt = np.cos(np.deg2rad(fld.coords[latn]))
    latw3,_ = xr.broadcast(lat_wgt,fld)
    #latw3 = latw3.transpose('time','lat','lon')
    latw3 = latw3.transpose(dims[0],dims[1],dims[2])
    latw3 = latw3.where(~fld.isnull(),np.nan)
    fldg = fld*latw3
    fld_ave = fldg.sum(dims[-2:])/latw3.sum(dims[-2:])
    #lat_wgt = lat_wgt/lat_wgt.sum()
    #fld_ave = np.average(fld,axis=lati,weights=lat_wgt).mean(axis=-1) # same as NCL's wgt_areaave()
    '''

    return fld_ave

def wgt_areaave (fld):
    ''' Calculates cos(lat) weighted area average for an xarray.DataArray object.
    Input 'fld' must be xarray.DataArray; for Numpy arrays, use np.average().
       
        Properly deals with (time-dependent?) missing values (e.g. ERSST)

    Note: This function gives the same result as wgt_areaave0 above and this is
        somewhat faster for large arrays e.g., dim = (2052, 144, 192).
    '''    

    if not hasattr(fld,'dims') or not hasattr(fld,'coords'):
       print("Input data must have 'dims' and 'coords' attributes.")
       print("Possibly not an xarray.DataArray.")
       return

    dims = fld.dims
    if 'lat' in dims:
       latn = 'lat'
       lati = dims.index('lat')
    elif 'latitude' in dims:
       latn = 'latitude'
       lati = dims.index('latitude')
    else:
       print('No valid latitude name!')
       return

    weights = np.cos(np.deg2rad(fld.coords[dims[lati]]))
    fld_ave = fld.weighted(weights).mean(dims[-2:])  # assumes the last 2 dims are lat,lon
    #fld_weighted = fld.weighted(weights)
    #fld_ave = fld_weighted.mean(dims[-2:])  # assumes the last 2 dims are lat,lon

    return fld_ave

def wgt_meanm (var10, lats=None):
    """
    Calculates the weightedof a geographical variable using latitude-based spatial weighting, handling
    missing values in one or both variables. Faster than wgt_areaave* above (but returns numpy array).
    
    Parameters:
    - var10 (2D array): Geographical variable (e.g., temperature) as a 2D array (lat x lon).
    
    Returns:
    - wgtMean (float): Weighted mean of var10.
    """

    if lats is None:
        if hasattr(var10,'lat'):
            lats = var10.lat
        elif hasattr(var10,'latitude'):
            lats = var10.latitude
        else:
            print("Input vars must have a latitude dimension if lats is None!")
            return

    var1 = np.array(var10)
    latitudes = np.array(lats)
    dim2 = tuple(np.arange(len(var1.shape)))[-2:]

    if var1.shape[-2] != latitudes.shape[0]:
        raise ValueError("Unequal latitude dimension!")
    
    # Convert latitudes to radians and calculate weights (cosine of latitude)
    weights = np.cos(np.radians(latitudes))

    # Ensure weights have the same shape as the variables
    weights_2d = np.tile(weights[:, np.newaxis], (1, var1.shape[-1]))
    
    # Mask missing values in var1
    valid_mask = ~np.isnan(var1)
    
    # Apply the mask to var1 and weights
    var1_masked = np.where(valid_mask, var1, np.nan)
    weights_masked = np.where(valid_mask, weights_2d, 0)  # Set weight to 0 for missing values
    
    # Calculate the weighted means for non-missing values
    wgtMean = np.nansum(var1_masked * weights_masked, axis=dim2) / np.sum(weights_masked, axis=dim2)
    
    return wgtMean

def wgt_variance (fld):
    ''' Calculates lat weighted spatial variance for an xarray.DataArray object.
    Input 'fld' must be xarray.DataArray; for Numpy arrays, use np.average().
    No NaNs are allowed. 
    '''    

    if not hasattr(fld,'dims') or not hasattr(fld,'coords'):
       print("Input data must have 'dims' and 'coords' attributes.")
       print("Possibly not a xarray.DataArray.")
       sys.exit()

    dims = fld.dims
    if 'lat' in dims:
       latn = 'lat'
       lati = dims.index('lat')
    elif 'latitude' in dims:
       latn = 'latitude'
       lati = dims.index('latitude')
    else:
       print ('No valid latitude name!')
       sys.exit()

    lat_wgt = np.cos(np.deg2rad(fld.coords[latn]))
    lat_wgt = lat_wgt/lat_wgt.sum()
    fld_ave = np.average(fld,axis=lati,weights=lat_wgt).mean(axis=-1) # same as NCL's wgt_areaave()
    fld_ano = np.abs(fld-fld_ave)**2
    fld_var = np.average(fld_ano,axis=lati,weights=lat_wgt).mean(axis=-1)

    return fld_var, fld_ave

def wgt_rmse (fldx,fldy,mean=False):
    ''' Calculates lat weighted spatial RMSE for two xarray.DataArray objects.
    Input 'fldx'is "obs"; for Numpy arrays, use np.average().
    No NaNs are allowed. By default, the spatial means are not subtracted.
    '''    

    if not hasattr(fldx,'dims') or not hasattr(fldx,'coords'):
       print("Input data must have 'dims' and 'coords' attributes.")
       print("Possibly not a xarray.DataArray.")
       return
    if not hasattr(fldy,'dims') or not hasattr(fldy,'coords'):
       print("Input data must have 'dims' and 'coords' attributes.")
       print("Possibly not a xarray.DataArray.")
       return

    if fldx.shape != fldy.shape:
       print("Two xarray.DataArray objects must be the same shape.")
       return

    dims = fldx.dims
    if 'lat' in dims:
       latn = 'lat'
       lati = dims.index('lat')
    elif 'latitude' in dims:
       latn = 'latitude'
       lati = dims.index('latitude')
    else:
       print('No valid latitude name!')
       return

    lat_wgt = np.cos(np.deg2rad(fldx.coords[latn]))
    lat_wgt = lat_wgt/lat_wgt.sum()

    if mean:
       fldx_ave = np.average(fldx,axis=lati,weights=lat_wgt).mean(axis=-1) # same as NCL's wgt_areaave()
       fldy_ave = np.average(fldy,axis=lati,weights=lat_wgt).mean(axis=-1) # same as NCL's wgt_areaave()
    else:
       fldx_ave = 0.0
       fldy_ave = 0.0

    fldx_ano = fldx-fldx_ave
    fldy_ano = fldy-fldy_ave

    patt_rmse = np.sqrt(np.average((fldy_ano-fldx_ano)**2,axis=lati,weights=lat_wgt).mean(axis=-1))

    return patt_rmse, fldx_ave, fldy_ave

def pattCorr1 (fldx,fldy):
    ''' Calculates lat weighted pattern correlation between two xarray.DataArray objects.
    Input 'fld' must be xarray.DataArray; for Numpy arrays, use np.average().
    No NaNs are allowed; use pattCorrm for arrays with missing values. 
    '''    

    if not hasattr(fldx,'dims') or not hasattr(fldx,'coords'):
       print("Input data must have 'dims' and 'coords' attributes!")
       print("Possibly not an xarray.DataArray.")
       return
    if not hasattr(fldy,'dims') or not hasattr(fldy,'coords'):
       print("Input data must have 'dims' and 'coords' attributes!")
       print("Possibly not an xarray.DataArray.")
       return

    if fldx.shape != fldy.shape:
       print("Two xarray.DataArray objects must be the same shape!")
       return

    dims = fldx.dims
    if 'lat' in dims:
       latn = 'lat'
       lati = dims.index('lat')
    elif 'latitude' in dims:
       latn = 'latitude'
       lati = dims.index('latitude')
    else:
       print('No valid latitude name!')
       return

    lat_wgt = np.cos(np.deg2rad(fldx.coords[latn]))
    lat_wgt = lat_wgt/lat_wgt.sum()

    fldx_ave = np.average(fldx,axis=lati,weights=lat_wgt).mean(axis=-1) # same as NCL's wgt_areaave()
    fldx_ano = fldx-fldx_ave
    fldx_var = np.average(np.abs(fldx_ano)**2,axis=lati,weights=lat_wgt).mean(axis=-1)

    fldy_ave = np.average(fldy,axis=lati,weights=lat_wgt).mean(axis=-1) # same as NCL's wgt_areaave()
    fldy_ano = fldy-fldy_ave
    fldy_var = np.average(np.abs(fldy_ano)**2,axis=lati,weights=lat_wgt).mean(axis=-1)

    patt_rmse = np.sqrt(np.average(np.abs(fldy-fldx)**2,axis=lati,weights=lat_wgt).mean(axis=-1)) # as in NCL
    #patt_rmse = np.sqrt(np.average(np.abs(fldy_ano-fldx_ano)**2,axis=lati,weights=lat_wgt).mean(axis=-1))

    patt_corr = np.average(fldx_ano*fldy_ano,axis=lati,weights=lat_wgt).mean(axis=-1)
    patt_corr = patt_corr/np.sqrt(fldx_var*fldy_var) 

    return patt_corr,patt_rmse,fldx_var,fldy_var,fldx_ave,fldy_ave

def pattCorr (var10, var20, lats):
    """
    Calculates the weighted pattern correlation coefficient between two
    geographical variables using latitude-based spatial weighting.
    
    Parameters:
    - var10 (2D array): First geographical variable (e.g., temperature) as a 2D array (lat x lon).
    - var20 (2D array): Second geographical variable as a 2D array (lat x lon).
    - lats  (1D array): Array of latitude values (in degrees) for each row in var1 and var2.
    
    Returns:
    - weighted_corr (float): Weighted pattern correlation coefficient between var1 and var2.

    By ChatGPT (14-NOV-2024), around 7 times faster than pattCorr1 above (which calculates more stats)
    """
    # Check if var1 and var2 have the same shape

    var1 = np.array(var10)
    var2 = np.array(var20)
    latitudes = np.array(lats)

    if var1.shape != var2.shape:
        raise ValueError("The two input variables must have the same shape.")
    
    # Convert latitudes to radians and calculate weights (cosine of latitude)
    weights = np.cos(np.radians(latitudes))
    
    # Ensure weights have the same shape as the variables
    weights_2d = np.tile(weights[:, np.newaxis], (1, var1.shape[1]))
    
    # Calculate the weighted means
    mean1 = np.average(var1, weights=weights_2d)
    mean2 = np.average(var2, weights=weights_2d)
    
    # Compute the anomalies
    anom1 = var1 - mean1
    anom2 = var2 - mean2
    
    # Compute the weighted covariance and variances
    covariance = np.sum(weights_2d * anom1 * anom2)
    variance1 = np.sum(weights_2d * anom1**2)
    variance2 = np.sum(weights_2d * anom2**2)
    
    # Calculate the weighted correlation
    weighted_corr = covariance / np.sqrt(variance1 * variance2)
    
    return weighted_corr

def pattCorrm(var10, var20, lats=None):
    """
    Calculates the weighted pattern correlation coefficient between two
    geographical variables using latitude-based spatial weighting, handling
    missing values in one or both variables.
    
    Parameters:
    - var10 (2D array): First geographical variable (e.g., temperature) as a 2D array (lat x lon).
    - var20 (2D array): Second geographical variable as a 2D array (lat x lon).
    - lats (1D array): Array of latitude values (in degrees) for each row in var1 and var2.
    
    Returns:
    - weighted_corr (float): Weighted pattern correlation coefficient between var1 and var2.

    By ChatGPT (14-NOV-2024), (this allows for missing values); 4-5 times faster than pattCorr1.
    """

    if lats is None:
        if hasattr(var10,'lat'):
            lats = var10.lat
        elif hasattr(var10,'latitude'):
            lats = var10.latitude
        else:
            print("Input vars must have a latitude dimension if lats is None!")
            return

    var1 = np.array(var10)
    var2 = np.array(var20)
    latitudes = np.array(lats)

    if var1.shape != var2.shape:
        raise ValueError("The two input variables must have the same shape!")
    
    # Convert latitudes to radians and calculate weights (cosine of latitude)
    weights = np.cos(np.radians(latitudes))

    # Ensure weights have the same shape as the variables
    weights_2d = np.tile(weights[:, np.newaxis], (1, var1.shape[1]))
    
    # Mask missing values in var1 and var2
    valid_mask = ~np.isnan(var1) & ~np.isnan(var2)
    
    # Apply the mask to var1, var2, and weights
    var1_masked = np.where(valid_mask, var1, np.nan)
    var2_masked = np.where(valid_mask, var2, np.nan)
    weights_masked = np.where(valid_mask, weights_2d, 0)  # Set weight to 0 for missing values
    
    # Calculate the weighted means for non-missing values
    mean1 = np.nansum(var1_masked * weights_masked) / np.sum(weights_masked)
    mean2 = np.nansum(var2_masked * weights_masked) / np.sum(weights_masked)
    
    # Compute the anomalies
    anom1 = np.where(valid_mask, var1_masked - mean1, 0)
    anom2 = np.where(valid_mask, var2_masked - mean2, 0)
    
    # Compute the weighted covariance and variances
    covariance = np.nansum(weights_masked * anom1 * anom2)
    variance1 = np.nansum(weights_masked * anom1**2)
    variance2 = np.nansum(weights_masked * anom2**2)
    
    # Calculate the weighted correlation
    weighted_corr = covariance / np.sqrt(variance1 * variance2) if variance1 > 0 and variance2 > 0 else np.nan
    
    return weighted_corr

def taylor_stats(fldx,fldy):
    '''Caluculate Taylor statistics for Taylor Diagram. The calculation follows that of
    NCL routine taylor_stats. The results match closely those from NCL. Normally, fldx
    is reference and fldy is model simulation. Bias is calculated as in:
        https://www.ncl.ucar.edu/Document/Functions/Contributed/taylor_stats.shtml

    This function returns a pd.Series(), with x- and y-stats re-ordered (otherwise, same as
    taylor_stats_or() below).
    '''
 
    #varx,avex = wgt_variance(fldx)
    #vary,avey = wgt_variance(fldy)
    pcor,rmse,varx,vary,avex,avey = pattCorr1 (fldx,fldy)
    stdr = np.sqrt(vary/varx)
    #rmse = np.sqrt(wgt_areaave(((fldy-avey)-(fldx-avex))**2))
    #rmse = np.sqrt((1-pcor**2)*vary)
    if avex == 0:
       bias = np.NaN
    else:
       bias = 100*(avey-avex)/avex

    score = 4*(1+pcor)**4/(((stdr+1/stdr)**2)*16)  # Eq. 5 of Taylor (2001), assuming max_corr, R_0 = 1

    stats_names = ['PCORR','STDVR','BIAS','AVEx','AVEy','VARx','VARy','RMSE','SCORE']
    stats = [pcor,stdr,bias,avex,avey,varx,vary,rmse,score]
    return pd.Series(stats,index=stats_names)

def lonFlip (x):
    ''' Flip longitudes from -180=>175 to 0->255
    '''

    dimx = x.dims
    if dimx[-1] not in ['lon','longitude']:
       print("The rightmost dim must be lon!")
       return

    mlon = x.shape[-1]
    if mlon%2 != 0:
       print('Longitude number must be even!')
       return

    mlon2 = mlon//2
    temp = x.copy()
    temp[...,0:mlon2] = x[...,mlon2:].values
    temp[...,mlon2:]  = x[...,0:mlon2].values
   
    xlon = x[dimx[-1]]
    #tlon = xlon.values
    if xlon[0] >= 0.:                              # (say) 0=>355
        #xlon[0:mlon2] = tlon[mlon2:] - 360
        #xlon[mlon2:]  = tlon[0:mlon2]
        xlon = xlon-180.
    else:                                          # (say) -180=>175
        #xlon[0:mlon2] = tlon[mlon2:]
        #xlon[mlon2:]  = tlon[0:mlon2] + 360
        xlon = (xlon+180.)%360

    if dimx[-1] == 'longitude':
        temp = temp.assign_coords(longitude=xlon)
    elif dimx[-1] == 'lon':
        temp = temp.assign_coords(lon=xlon)

    return temp

def commonality_analysis(y, X):
    """
    Perform commonality analysis for a multiple regression model.

    Parameters
    ----------
    X : pandas.DataFrame or ndarray
        Predictor variables.
    y : array-like
        Response variable.

    Returns
    -------
    pandas.DataFrame
        Unique and shared variance contributions for each predictor subset.

    Commonality coefficients (unique + shared contributions):
              Commonality
    X1               0.245082    # => unique X1 contribution to the expalined y-variance, excluding X2/X3
    X2               0.141041
    X3               0.097478
    X1 & X2 & X3     0.012646    # shared y-variance explained by X1,X2,X3 together
    X2 & X3         -0.011536    # shared y-variance explained by X2 and X3 together
    X1 & X3         -0.048276
    X1 & X2         -0.089396

    My comments: This function uses Statsmodels OLS function, but gives exactly the same results 
                 as the sklearn's LinearRegression function of commonality_analysis_sk below, as
                 the two functions use the same algorithm.
                 See:
                   comp_varianceDecomp_MLR5.py
                   comp_CommonalityAnalysisMLR_Copilot.py
    in: ~/Library/CloudStorage/OneDrive-CSIRO/workDir/Eval_CMIP6/CMIP6_MME/forcedSig_workdir_Revision

    This function is approx. twice as fast as commonality_analysis_sk().

    Code by ChatGPT
    27-AUG-2025
    """

    import itertools
    import statsmodels.api as sm

    if isinstance(X, np.ndarray):
        X = pd.DataFrame(X, columns=[f"X{i+1}" for i in range(X.shape[1])])
    
    predictors = X.columns.tolist()
    results = {}

    # Iterate over all subsets of predictors
    for k in range(1, len(predictors)+1):
        for subset in itertools.combinations(predictors, k):
            X_subset = sm.add_constant(X[list(subset)])
            model = sm.OLS(y, X_subset).fit()
            results[subset] = model.rsquared

    # Calculate commonality coefficients
    commonalities = {}
    for k in range(1, len(predictors)+1):
        for subset in itertools.combinations(predictors, k):
            # Inclusion-exclusion principle
            value = 0
            for j in range(1, len(subset)+1):
                for subsubset in itertools.combinations(subset, j):
                    sign = (-1)**(len(subset)-j)
                    value += sign * results[subsubset]
            commonalities[subset] = value

    # Format results
    df = pd.DataFrame.from_dict(commonalities, orient='index', columns=['Commonality'])
    df.index = [" & ".join(s) for s in df.index]
    df = df.sort_values(by="Commonality", ascending=False)
    return df["Commonality"]*100   # return percent variances

def commonality_analysis_sk(y, X):
    """
    Perform commonality analysis on multiple regression models.
    
    Parameters:
    - X: pandas DataFrame of predictors
    - y: pandas Series or array-like of dependent variable
    
    Returns:
    - Dictionary of R² contributions for each combination of predictors

    My comments: This function uses sklearn's LinearRegression function, but gives exactly 
                 the same results as the Statsmodels version of commonality_analysis above.
                 See:
                   comp_varianceDecomp_MLR5.py
                   comp_CommonalityAnalysisMLR_Copilot.py
    in: ~/Library/CloudStorage/OneDrive-CSIRO/workDir/Eval_CMIP6/CMIP6_MME/forcedSig_workdir_Revision

    Code by Copilot
    27-AUG-2025
    """

    import itertools
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import r2_score

    predictors = X.columns.tolist()
    results = {}

    # Iterate over all non-empty combinations of predictors
    for r in range(1, len(predictors) + 1):
        for combo in itertools.combinations(predictors, r):
            model = LinearRegression()
            model.fit(X[list(combo)], y)
            y_pred = model.predict(X[list(combo)])
            r2 = r2_score(y, y_pred)
            results[combo] = r2

    # Compute commonality coefficients
    commonality = {}
    for combo in results:
        combo_set = set(combo)
        shared_r2 = results[combo]
        for sub_r in range(1, len(combo)):
            for sub_combo in itertools.combinations(combo, sub_r):
                shared_r2 -= commonality.get(sub_combo, 0)
        commonality[combo] = shared_r2

    return commonality

def make_test_array(ntimes=100, ncolumns=1000,
                    y0=0.2, yc=1.2, ys=0.5, yrand=1,
                    seed=0):
    """
    Test with a larger array. To keep things simple, only the random component 
    will vary from one column to the next. This also lets us do an empirical test of 
    the estimated parameter error bars.

    (From https://currents.soest.hawaii.edu/ocn_data_analysis/_static/regression.html).
    """

    # frequency in cycles per time unit:
    freq = 1

    t = np.linspace(0, 10, ntimes)

    xc = np.cos(2 * np.pi * freq * t)
    xs = np.sin(2 * np.pi * freq * t)

    xmod = np.ones((ntimes, 3), float)
    xmod[:, 1] = xc
    xmod[:, 2] = xs
    
    np.random.seed(seed)  # make the "random" numbers repeatable
    y = y0 + yc * xc + ys * xs
    y = y[:, np.newaxis] + yrand * np.random.randn(ntimes, ncolumns)
    return y, xmod

def mean_confidence_interval(data, axis=0, confidence=0.95):
    """
    Compute the confidence interval for a single series mean based on t-test.

    The same result can also be obtained by the two following ways:
    scipy.stat.t.interval(0.95, len(data)-1, loc=np.mean(dataa), scale=scipy.stat.sem(dataa))
    statsmodels.stats.api.DescrStatsW(data).tconfint_mean()
    """

    a = 1.0 * np.array(data)
    n = a.shape[axis]
    m, se = np.mean(a, axis=axis), scipy.stats.sem(a, axis=axis)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return np.asarray((m-h, m, m+h)).T

def get_weights (wlen,window='hanning'):
    """
    Get weights for a window with given length. Available windows are:

    See: https://docs.scipy.org/doc/scipy/reference/signal.windows.html 
         for available windows
    """

    windows = ['barthann', 'bartlett', 'blackman', 'blackmanharris', 'bohman', 'boxcar',
              'chebwin', 'cosine', 'dpss', 'exponential', 'flattop', 'gaussian',
              'general_cosine', 'general_gaussian', 'general_hamming', 'get_window',
              'hamming', 'hann', 'kaiser', 'kaiser_bessel_derived', 'nuttall', 'parzen',
              'taylor', 'triang', 'tukey']

    if window == 'flat': window = 'boxcar'
    if window == 'hanning': window = 'hann'

    if window in windows:
        import scipy.signal as sig
        if wlen < 3: raise ValueError("Window length must be at least 3.")
        if not wlen % 2:  # window_len is even
            wlen += 1
            print("Window length reset to {}".format(wlen))
        w = sig.get_window (window, wlen, fftbins=False)
    else:
        msg = "Unrecognized window type '{}'".format(window)
        print(msg + " Defaulting to np.hanning")
        w = np.hanning(wlen)

    return w / w.sum()

"""
The following three functions are originally from QuantEcon.py package (pip install quantecon):
    https://quantecon.org/quantecon-py/
    https://github.com/QuantEcon/QuantEcon.py/blob/master/quantecon/estspec.py

    with my modifications.
"""

def smooth (x, window_len=7, window='hanning'):
    """
    Smooth the data in x using convolution with a window of requested
    size and type.

    Parameters
    ----------
    x : array_like(float)
        A flat NumPy array containing the data to smooth
    window_len : scalar(int), optional
        An odd integer giving the length of the window.  Defaults to 7.
    window : string
        A string giving the window type. Possible values are 'flat',
        'hanning', 'hamming', 'bartlett' or 'blackman'
    See: https://docs.scipy.org/doc/scipy/reference/signal.windows.html 
         for available windows

    Returns
    -------
    array_like(float)
        The smoothed values

    Notes
    -----
    Application of the smoothing window at the top and bottom of x is
    done by reflecting x around these points to extend it sufficiently
    in each direction.

    This function is faster than pd.rolling() (2.35 times). Also, this doesn't loose
    data at both ends.
    """
    if len(x) < window_len:
        raise ValueError("Input vector length must be >= window length.")

    if window_len < 3:
        raise ValueError("Window length must be at least 3.")

    if not window_len % 2:  # window_len is even
        window_len += 1
        print("Window length reset to {}".format(window_len))

    windows = {'hanning': np.hanning,
               'hamming': np.hamming,
               'bartlett': np.bartlett,
               'blackman': np.blackman,
               'flat': np.ones  # moving average
               }

    # === Reflect x around x[0] and x[-1] prior to convolution === #
    k = window_len // 2
    xb = x[:k]   # First k elements
    xt = x[-k:]  # Last k elements
    s = np.concatenate((xb[::-1], x, xt[::-1]))

    # === Select window values === #
    if window in windows.keys():
        w = windows[window](window_len)
    else:
        msg = "Unrecognized window type '{}'".format(window)
        print(msg + " Defaulting to hanning")
        w = windows['hanning'](window_len)

    return np.convolve(s, w / w.sum(), mode='valid')

def smooth0 (x, window_len=7, window='hanning'):
    if len(x) < window_len:
        raise ValueError("Input vector length must be >= window length.")

    if window_len < 3:
        raise ValueError("Window length must be at least 3.")

    if not window_len % 2:  # window_len is even
        window_len += 1
        print("Window length reset to {}".format(window_len))

    windows = {'hanning': np.hanning,
               'hamming': np.hamming,
               'bartlett': np.bartlett,
               'blackman': np.blackman,
               'flat': np.ones  # moving average
               }

    # === Reflect x around x[0] and x[-1] prior to convolution === #
    k = int(window_len / 2)
    xb = x[:k]   # First k elements
    xt = x[-k:]  # Last k elements
    s = np.concatenate((xb[::-1], x, xt[::-1]))

    # === Select window values === #
    if window in windows.keys():
        w = windows[window](window_len)
    else:
        msg = "Unrecognized window type '{}'".format(window)
        print(msg + " Defaulting to hanning")
        w = windows['hanning'](window_len)

    return np.convolve(w / w.sum(), s, mode='valid')

def smooth_df(df, window_len=7, window='hanning'):
    """
    Smooth the data in x using convolution with a window of requested
    size and type.

    Parameters
    ----------
    df : A pandas DataFrame, containing the data to smooth
    window_len : scalar(int), optional
        An odd integer giving the length of the window.  Defaults to 7.
    window : string
        A string giving the window type. Possible values are 'flat',
        'hanning', 'hamming', 'bartlett' or 'blackman'

    Returns
    -------
    array_like(float)
        The smoothed values

    Notes
    -----
    Application of the smoothing window at the top and bottom of x is
    done by reflecting x around these points to extend it sufficiently
    in each direction.

    This function is faster than pd.rolling() (2.35 times). Also, this doesn't loose
    data at both ends.
    """

    if isinstance(df,pd.DataFrame):
        return df.apply(lambda x: smooth(x,window_len=window_len,window=window))
    else:
        y = smooth(df,window_len=window_len,window=window)
        if isinstance(df,pd.Series):
            y = pd.Series(y,index=df.index)
        return y

def spectrum(xi, window_len=11, window='hanning', fs=1, dtrend=0):
#def periodogram(x, window=None, window_len=7):
    """
    Example 4 (https://www.ncl.ucar.edu/Document/Functions/Built-in/specx_anal.shtml)

    The following sequence is the order in which the underlying specx_anal code computes the spectrum:
   [1] detrend the series [optional]
   [2] taper the series   [optional]
   [3] calculate the variance of the detrended/tapered series
   [4] forward fft on series
   [5] square the coef [periodogram  ~2 dof]  
   [6] smooth the periodogram estimates 
   [7] normalize [6] so that the area under the curve is
       equal to the variance calculated in [3]
    
        area_under_curve =  SUM { S(f)*df*frac }
        
    where frac=1.0 except the beginning and end values where frac=0.5

    The units are variance/(unit frequency interval)

    Parameters
    ----------
    xi : 1-d array_like(float)
        A flat NumPy array containing the data to analyse
    window : string
        A string giving the window type. Possible values are 'flat',
        'hanning' (default), 'hamming', 'bartlett' or 'blackman'
    window_len : scalar(int), optional(default=11)
        An odd integer giving the length of the window.  Defaults to 11.
    fs : Sampling frequency ( = 1/month or 12/year for monthly data)
    dtrend: No detrending (=0, default), 1st or 2nd-order detrending (= 1, 2)

    Returns
    -------
    w : array_like(float)
        Fourier frequences at which spectrum is evaluated
    I_w : array_like(float)
        Values of spectrum at the Fourier frequences

    Refs:
       https://currents.soest.hawaii.edu/ocn_data_analysis/_static/Spectrum.html
       https://www.ncl.ucar.edu/Document/Functions/Built-in/specx_anal.shtml (example 4)

    Similar speeds for spectrum and spectrum0 below.
    """

    n = len(xi)
    nh = n//2+1
    if dtrend in [1,2]:
       x0 = detrend(xi,dtrend)
    else:
       x0 = xi
    varx0 = x0.var()
    winweights = taper(n,0.1)
    x = x0 * winweights
    varx = x.var()
    I_w = np.abs(np.fft.fft(x))**2 / n
    #w = 2 * np.pi * np.arange(n) / n  # Fourier frequencies
    w = fs * np.arange(n) / n  # Fourier frequencies (changed to linear freqs) =>> np.fft.fftfreq(n,1/fs)[:nh]
    w, I_w = w[:nh], I_w[:nh]  # Take only values on [0, pi]
    if window:
        I_w = smooth(I_w, window_len=window_len, window=window)
    spec_vals = 2*I_w          # multiplying by 2 keeps the observed variance
    frac = np.ones(nh)
    frac[0] = 0.5
    frac[-1] = 0.5
    df = w[1]-w[0]
    spec_area = (spec_vals*df*frac).sum()
    spec_vals = spec_vals*varx0/spec_area
    if isinstance(x,pd.Series):
        return pd.Series(spec_vals,index=w)
    else:
        return w, spec_vals

def spectrum0(x0, window_len=11, window='hanning'):
#def periodogram(x, window=None, window_len=7):
    r"""
    Computes the periodogram

    .. math::

        I(w) = \frac{1}{n} \Big[ \sum_{t=0}^{n-1} x_t e^{itw} \Big] ^2

    at the Fourier frequences :math:`w_j := \frac{2 \pi j}{n}`,
    :math:`j = 0, \dots, n - 1`, using the fast Fourier transform. Only the
    frequences :math:`w_j` in :math:`[0, \pi]` and corresponding values
    :math:`I(w_j)` are returned. If a window type is given then smoothing
    is performed.

    Parameters
    ----------
    x : 1-d array_like(float)
        A flat NumPy array containing the data to analyse
    window : string
        A string giving the window type. Possible values are 'flat',
        'hanning' (default), 'hamming', 'bartlett' or 'blackman'
    window_len : scalar(int), optional(default=11)
        An odd integer giving the length of the window.  Defaults to 11.

    Returns
    -------
    w : array_like(float)
        Fourier frequences at which spectrum is evaluated
    I_w : array_like(float)
        Values of spectrum at the Fourier frequences

    Refs:
       https://currents.soest.hawaii.edu/ocn_data_analysis/_static/Spectrum.html
       https://www.ncl.ucar.edu/Document/Functions/Built-in/specx_anal.shtml (example 4)
    """

    n = len(x0)
    #if dtrend in [1,2]:
    #   h_detrended = detrend(x,dtrend)
    #else:
    #   h_detrended = h
    varx0 = x0.var()
    winweights = taper(n,0.1)
    x = x0 * winweights
    I_w = np.abs(np.fft.fft(x))**2 / n
    #w = 2 * np.pi * np.arange(n) / n  # Fourier frequencies
    w = np.arange(n) / n  # Fourier frequencies (I changed to linear freqs)
    w, I_w = w[:int(n/2)+1], I_w[:int(n/2)+1]  # Take only values on [0, pi]
    if window:
        I_w = smooth(I_w, window_len=window_len, window=window)
    spec_vals = 2*I_w*varx0/x.var()       # multiplying by 2 keeps the observed variance
    if isinstance(x,pd.Series):
        return pd.Series(spec_vals,index=w)
    else:
        return w, spec_vals

def ar_spectrum(x, window_len=11, window='hanning'):
#def ar_periodogram(x, window='hanning', window_len=7):
    """
    Compute periodogram from data x, using prewhitening, smoothing and
    recoloring.  The data is fitted to an AR(1) model for prewhitening,
    and the residuals are used to compute a first-pass periodogram with
    smoothing.  The fitted coefficients are then used for recoloring.
  
    My note: The theory behind pre-whitenning is explained at:
       https://python-advanced.quantecon.org/estspec.html

    The returned arrays are shorter by 1 than those returned by "spectrum",
    because the input is a lag-1 ts (and hence shorter by 1 data point). 

    Parameters
    ----------
    x : array_like(float)
        A flat NumPy array containing the data to smooth
    window_len : scalar(int), optional
        An odd integer giving the length of the window.  Defaults to 7.
    window : string
        A string giving the window type. Possible values are 'flat',
        'hanning', 'hamming', 'bartlett' or 'blackman'

    Returns
    -------
    w : array_like(float)
        Fourier frequences at which periodogram is evaluated
    I_w : array_like(float)
        Values of periodogram at the Fourier frequences

    """
    # === run regression === #
    x_lag = x[:-1]  # lagged x
    X = np.array([np.ones(len(x_lag)), x_lag]).T  # add constant

    y = np.array(x[1:])  # current x

    beta_hat = np.linalg.solve(X.T @ X, X.T @ y)  # solve for beta hat
    e_hat = y - X @ beta_hat  # compute residuals
    phi = beta_hat[1]  # pull out phi parameter

    # === compute periodogram on residuals === #
    w, I_w = spectrum(e_hat, window=window, window_len=window_len)
    #w, I_w = periodogram(e_hat, window=window, window_len=window_len)

    # === recolor and return === #
    I_w = I_w / np.abs(1 - phi * np.exp(1j * 2 * np.pi * w))**2

    return w, I_w

def df_autocorr(df, lag=[1], axis=0):
    """Compute full-sample column-wise autocorrelation for a DataFrame."""

    if len(lag) == 1:
        return df.apply(lambda col: col.autocorr(lag[0]), axis=axis)
    else:
        corrs = []
        for l in lag:
            corrs.append(df.apply(lambda col: col.autocorr(l), axis=axis))
      
        CorrCoef = pd.concat(corrs,axis=1)
        CorrCoef.columns = lag
        return CorrCoef 
 
def df_rolling_autocorr(df, window=None, lag=1):
    """Compute rolling column-wise autocorrelation for a DataFrame.
    
    For full length autocorr, set window = len(df).
    """

    if not window: window = df.shape[0]
    return (df.rolling(window=window).corr(df.shift(lag))).dropna()

def rmse (x,y):
    """
    Calculate RMSE between two numpy arrays of same dimension, or between two
    pandas DataFrames, a DataFrames and Series, or two Series.

    Use wgt_rmse for area wighted verion of RMSE.
    """

    if isinstance(x,pd.DataFrame) or isinstance(x,pd.Series) and \
       isinstance(y,pd.DataFrame) or isinstance(y,pd.Series):
       if isinstance(x,pd.DataFrame) and isinstance(y,pd.Series):
           rmse_ens = np.sqrt((x.subtract(y,axis=0)**2).mean(axis=0))
       else:
           rmse_ens = np.sqrt((x.subtract(y)**2).mean(axis=0))
    else:
       if x.shape == y.shape:
           rmse_ens = np.sqrt((np.subtract(x,y)**2).mean())
       else:
           print('Numpy arrays of unequal dimensions!')
           return

    return rmse_ens

def dict_swap (dict_flds, index=None):
    """Takes a dictionary of pd.DataFrames and returns a new dictionary containing
    dataframes, with keys of original dict as columns and columns of original dict 
    as keys of the new dict.
    """
  
    df_dict = dict()
    cols = dict_flds[list(dict_flds.keys())[0]].columns
    for c in cols:
        temp = pd.DataFrame({i:v[c] for i,v in dict_flds.items() if c in v.columns})
        if index is not None and temp.shape[0]==len(index):
            temp.index = index
        df_dict[c] = temp

    return df_dict

def get_EnsNames (columns, obs='HadCRUT5'):
    """Collects all ensemble members of individual models in a dictionary and returns.

    Input:
       A (list of) columns/index of pandas DataFrame/Series
    Output:
       mod_ens => Dictionary containing ensemble members of individual models

    """

    if isinstance(columns,pd.Series):    # pd.DataFrames seem to work!
        print("Input must be a columns/index of pandas DataFrame/Series!")
        return

    models = list(set([m.split('_')[0] for m in columns])) # set is used to remove the duplicate names
    models.sort()
    if obs in columns:
        move_list_item(models, obs, 0) # set() arranges in alphabetical order; move obs back to front
    if 'CMIP6' in models:
        models.remove('CMIP6')
        models.insert(1,'CMIP6_ensm')
    mod_ens = {}
    for m in models:
        ens_num = [v for v in columns if m+'_r' in v] 
        mod_ens[m] = ens_num

    if obs in columns:
        mod_ens[obs] = obs
    if 'CMIP6_ensm' in columns:
        mod_ens['CMIP6_ensm'] = 'CMIP6_ensm'

    return mod_ens

def get_EnsWgts (columns, obs='HadCRUT5'):
    """Build a weight array same size as columns:

          df_enswt = 1/(N*M_i), N = number of models and M_i = ens_num for model M

    This may be used to compute weighted stats of CMIP6 ensemble; see, IPCC AR6 report, 
    chap 3, page 429.

    Input:
       A list of columns/index of pandas DataFrame/Series
    Output:
       df_enswt => A pandas series containing weights for applying to individual ensemble members
    of individual models of CMIP6, before calculating CMIP6 ensemble mean, as:

        (df_enswt*df_tas[df_enswt.index]).sum(axis=1) # see get_tsEnsm0 below

    This method of calculating CMIP6_ensm is equivalent to (is faster than):

        df_tasm,ens_tas = ms.get_tsEnsm(df_tas)
        df_tas_ensm = df_tasm.mean(axis=1)
    """

    if isinstance(columns,pd.DataFrame):
        columns = columns.columns

    if obs == '':
        drop_list = [c for c in columns if '_ensm' in c]
    else:
        drop_list = [obs] + [c for c in columns if '_ensm' in c]
    columns_v2 = columns.drop(drop_list)
    ens_num = get_EnsNames(columns_v2)
    df_enswt = pd.Series(index=columns_v2,dtype='float')
    #df_enswt[:]=1
    nmods = len(ens_num.keys())
    for m in ens_num.keys():
        df_enswt[ens_num[m]] = 1./(nmods*len(ens_num[m]))

    return df_enswt

def get_tsEnsm (df_tas, obs='HadCRUT5', ensnum=True):
    """Calculate the separate ensemble-mean timeseries for each model 
       from the CMIP6 ensemble. Specifically, get a multi-model, multi-ensemble member
       dataframe of CMIP6 data from df_tas, and:

          1) Calculate the ensemble means for each model
          3) Return the DataFrames

    Input:
       df_tas => a DataFrame of  multi-model, multi-ensemble member data

    #CMIP6 method (IPCC AR6 report, chap 3, page 429):

    drop_list = [obs] + [c for c in df_tas.columns if '_ensm' in c]
    df_tas_v2 = df_tas.drop(drop_list,axis=1)
    ens_num1 = ms.get_EnsNames(df_tas_v2)
    df_enswt = pd.Series(index=df_tas_v2.columns,dtype='int')
    df_enswt[:]=1
    nmods = len(ens_num1.keys())
    for m in ens_num1.keys():
        df_enswt[ens_num1[m]] = 1./(nmods*len(ens_num1[m]))
    
    df_tasm_cmip6 = (df_enswt*df_tas_v2).sum(axis=1) # same as df_tasm returned by this function
    See function get_tsEnsm0 below.
    """

    if isinstance(df_tas,pd.Series):
        columns = df_tas.index
    else:
        columns = df_tas.columns
    models = list(set([m.split('_')[0] for m in columns])) # set is used to remove the duplicate names
    models.sort()
    if obs in columns:
        move_list_item(models, obs, 0) # set() arranges in alphabetical order; move obs back to front
    if 'CMIP6' in models:
        models.remove('CMIP6')
        models.insert(1,'CMIP6_ensm')
    if isinstance(df_tas,pd.Series):
        df_tasm = pd.Series(index=models,dtype='float64')
    else:
        df_tasm = pd.DataFrame(columns=models)
    mod_ens = pd.Series(index=models,dtype='int')
    for m in models:
        ens_num = [v for v in columns if m+'_r' in v] # '_r' ensures picking only model ensemble members
        mod_ens[m] = len(ens_num)
        if isinstance(df_tas,pd.Series):
            df_tasm[m] = df_tas[ens_num].mean(axis=0)
        else:
            df_tasm[m] = df_tas[ens_num].mean(axis=1) 

    # Special treatment for OBS and CMIP6_ensm
    if obs in columns:
        df_tasm[obs] = df_tas[obs]
        mod_ens[obs] = 1
    if 'CMIP6_ensm' in columns:
        df_tasm['CMIP6_ensm'] = df_tas['CMIP6_ensm']
        mod_ens['CMIP6_ensm'] = mod_ens[2:].sum()

    if ensnum:
        return df_tasm,mod_ens
    else:
        return df_tasm

def get_tsEnsm0 (df_tas, obs='HadCRUT5'):
    """Calculate the grand ensemble-mean of CMIP6 simulations with different models
       having different numbers of ensemble members. Specifically, build a weight
       array same size as df_tas.shape[1]:

          df_enswt = 1/(N*M_i), N = number of models and M_i = ens_num for model M
       and take the weighted sum(axis=1). See, IPCC AR6 report, chap 3, page 429.

    This function is twice as fast as get_tsEnsm().

    # Simpler proof:

    x = np.asarray([2,3.4,4,5.1,2.3,1.1]) # 3 models with ens members: (m1r1,m2r1,m2r2,m2r3,m3r1,m3r2)
    w = np.asarray([1/3,1/9,1/9,1/9,1/6,1/6]) # weights: 1/(N*M_i), N=3 and_i = ens_num for model M
    (x*w).sum() == mean(2,mean(3.4,4,5.1,2.3),mean(2.3,1.1)) as in ms.get_tsEnsm0

    Input:
       df_tas => a DataFrame of  multi-model, multi-ensemble member data
       obs => name of OBS
       #retw => return weighted array, if retw=True
    Output:
       df_tasm => a pandas series/dataframe (retw=True) of  multi-model, multi-ensemble member 
                  grand mean
    """

    """
    drop_list = [obs] + [c for c in df_tas.columns if '_ensm' in c]
    df_tas_v2 = df_tas.drop(drop_list,axis=1)
    ens_num = get_EnsNames(df_tas_v2)
    df_enswt = pd.Series(index=df_tas_v2.columns,dtype='float')
    #df_enswt[:]=1
    nmods = len(ens_num.keys())
    for m in ens_num.keys():
        df_enswt[ens_num[m]] = 1./(nmods*len(ens_num[m]))
    """
    df_enswt = get_EnsWgts (df_tas.columns,obs=obs)

    df_tasm = (df_enswt*df_tas[df_enswt.index]).sum(axis=1) # = df_tasm from get_tsEnsm().mean(axis=1)
    df_tasm.name = 'CMIP6_ensm'
    return df_tasm

def season_wgt_mean (ds, calendar="standard"):
    """Calculate seaonal means of monthly mean data. Input data must be an xarray
    DataArray. This incorporates weighting for variable number_of_days in months.

    For unweighted seasonal means, use:
          ds_unweighted = ds.groupby("time.season").mean("time")

    From:
       https://docs.xarray.dev/en/stable/examples/monthly-means.html
    """
    # Make a DataArray with the number of days in each month, size = len(time)
    month_length = ds.time.dt.days_in_month

    # Calculate the weights by grouping by 'time.season'
    weights = (
        month_length.groupby("time.season") / month_length.groupby("time.season").sum()
    )

    # Test that the sum of the weights for each season is 1.0
    np.testing.assert_allclose(weights.groupby("time.season").sum().values, np.ones(4))

    # Calculate the weighted average
    return (ds * weights).groupby("time.season").sum(dim="time")

def season_mean_year (ds, calendar="standard"):
    """Calculate (unweighted) seaonal means of monthly mean data for individual years.
    Input data must be an xarray DataArray. Note, this doesn't incorporate weighting for
    variable number_of_days in months. But, see:
    https://stackoverflow.com/questions/59234745/is-there-any-easy-way-to-compute-seasonal-mean-with-xarray 

    For unweighted seasonal and all year means, use:
          ds_unweighted = ds.groupby("time.season").mean("time")

    """
    seasn = ['DJF','JJA','MAM','SON']
    dict_seas = {}
    for sea in seasn:
        ds_sm = ds[ds.time.dt.season==sea]
        dict_seas[sea] = ds_sm.groupby('time.year').mean('time')

    return dict_seas

def seas_means_df (df_data):
    """Calculates four-season means and anomalies of a dataframe: df_data. The input must
    be monthly data.

    Input:
        df_data => A DataFrame of monthly data
    Outputs:
        pd.DataFrame(seas_means_dict) => A DataFrame of seasonal means of df_data
        seas_anoms_dict => A dictionary of seasonal anomalies of df_data
    """

    if not isinstance(df_data,pd.DataFrame):
        print('Input data must be a pd.DataFrame object!')
        return

    seas_means = df_data.resample('QE-NOV').mean()  # seasonal means: method 1
    #seas_means = df_data.iloc[2:].resample('3M',closed='left').mean()  # seasonal means: method 2
    seas_dict = {'DJF':2,'MAM':5,'JJA':8,'SON':11}
    seas_means_dict = {}
    seas_anoms_dict = {}
    for k in seas_dict.keys():
        temp = seas_means[seas_means.index.month==seas_dict[k]]
        seas_means_dict[k] = temp.mean()
        seas_anoms_dict[k] = temp - seas_means_dict[k]

    return pd.DataFrame(seas_means_dict), seas_anoms_dict

def anomaly (data):
    """Calculates and removes the climatological annual cycle of a 1-d array. The latter must
    be monthly data. Works for numpy/xarray and pd.Series(). For pd.DataFrame(): 
            df_datao = df_data.apply(ms.anomaly) => df_datao = ms.anomaly_df(df_data)

    Input:
        data => A 1-d Series/numpy/xarray array of monthly data
    Outputs:
        datao => A numpy array of anomalies of data
    """

    if len(data.shape) > 1:
        print('Only 1-d arrays are permitted!')
        return
    else:
        dat2d = np.array(data).reshape([-1,12])
        return (dat2d - dat2d.mean(axis=0)[np.newaxis,:]).reshape(data.shape)

def anomaly_df (df_data,yrc12=None):
    """Calculates and removes the climatological annual cycle of a dataframe: df_data. The latter must
    be monthly data. Works for pd.Series() and pd.DataFrame(): 
            df_datao = df_data.apply(ms.anomaly) => df_datao = ms.anomaly_df(df_data)

    Input:
        df_data => A DataFrame of monthly data
        yrc12 => ['1850','1900'] if not None
    Outputs:
        df_datao => A DataFrame of anomalies of df_data
    """

    if hasattr(df_data,'index') and hasattr(df_data.index,'month'):
        df_datag = df_data.groupby(df_data.index.month) # group by calendar months
        if yrc12 is None:
            df_datao = df_datag.transform(lambda x: x-x.mean()) # remove the climatological monthly means
        else:
            yrc1 = yrc12[0]
            yrc2 = yrc12[1]
            df_datao = df_datag.transform(lambda x: x-x.loc[yrc1:yrc2].mean()) # remove the clim_means for a special period
    else:
        df_datao = df_data.apply(anomaly)

    return df_datao

def anomaly_xr (xr_data):
    """Calculates and removes the climatological annual cycle of a DataArray: xr_data. The latter must
    be monthly data. 

    Input:
        xr_data => A DataArray of monthly data
    Outputs:
        xr_datao => A DataArray of anomalies of xr_data
    """

    if hasattr(xr_data,'time'):
        xr_datag = xr_data.groupby('time.month') # group by calendar months
        xr_datao = xr_datag - xr_datag.mean()    # remove the climatological monthly means
    else:
        print("Data array doesn't have a time coordinate! Must be monthly xr.DataArray.")
        return

    return xr_datao

def lagClimMons_sr (ts,nyear=2):
    """ Return data with lagged climatological months from a series (pandas/xarray/numpy). 
    The calculations are useful for ENSO-related analysis.

    Inputs:
        ts = A pandas/xarray/numpy/list timeseries
        nyear = Lagged climatology for 2 or 3 years
    """

    if np.ndim(ts) != 1:
        print('Input must be a 1-d series')
        return

    nmon = 12
    calMons = ['Jan(-1)', 'Feb(-1)', 'Mar(-1)', 'Apr(-1)', 'May(-1)', 'Jun(-1)', \
               'Jul(-1)', 'Aug(-1)', 'Sep(-1)', 'Oct(-1)', 'Nov(-1)', 'Dec(-1)', \
               'Jan(0)', 'Feb(0)', 'Mar(0)', 'Apr(0)', 'May(0)', 'Jun(0)', \
               'Jul(0)', 'Aug(0)', 'Sep(0)', 'Oct(0)', 'Nov(0)', 'Dec(0)', \
               'Jan(+1)', 'Feb(+1)', 'Mar(+1)', 'Apr(+1)', 'May(+1)', 'Jun(+1)', \
               'Jul(+1)', 'Aug(+1)', 'Sep(+1)', 'Oct(+1)', 'Nov(+1)', 'Dec(+1)']
    #calMons = ["Jan(0)","Feb(0)","Mar(0)","Apr(0)","May(0)","Jun(0)", \
    #          "Jul(0)","Aug(0)","Sep(0)","Oct(0)","Nov(0)","Dec(0)", \
    #          "Jan(+1)","Feb(+1)","Mar(+1)","Apr(+1)","May(+1)","Jun(+1)", \
    #          "Jul(+1)","Aug(+1)","Sep(+1)","Oct(+1)","Nov(+1)","Dec(+1)"]
    #if isinstance(ts,np.ndarray):
    #    tmp = ts.reshape([-1,nmon])
    #else:
    #    tmp = np.array(ts).reshape([-1,nmon])

    tmp = np.array(ts).reshape([-1,nmon])

    if nyear == 3:
        #ym1 = [c.replace('+','-') for c in calMons[nmon:]]
        #calMons = ym1+calMons
        temp = np.concatenate([tmp[:-2,:],tmp[1:-1,:],tmp[2:,:]],axis=1)
    else:
        calMons = calMons[nmon:]  # discard the "minus" years
        temp = np.concatenate([tmp[:-1,:],tmp[1:,:]],axis=1)

    return pd.DataFrame(temp,columns=calMons)

def lagClimStat_sr_v0 (ts1,ts2,offset=2,endMon=-7,lstat='reg',lstd=False,nyear=2):
    """ Calculate lagged climatological regression/correlation between two pandas series. 
    The calculations are useful for ENSO-related analysis.

    Inputs:
        ts1 = Series 1
        ts2 = Series 2
        offset = Start (calendar) month or offset for ts2 w.r.t. ts1 (default = 2 [March])
        endMon = End (calendar) month, from the end of the second calendar year (default = -7 [May(+1)])
        lstat = Regression or correlation
        lstd =  If true, standardise ts1
        nyear = Lagged climatology for 2 or 3 years
    """
    if not isinstance(ts1,pd.Series) and not isinstance(ts2,pd.Series):
       print('Both inputs must be pd.Series')
       return 

    if endMon == 0: endMon = -1
    if endMon > 0:  endMon = -1*endMon
    if lstat == 'reg':
        sfunc = simpReg
    else:
        sfunc = simpCorr

    nmon = 12
    calMons = ["Jan(0)","Feb(0)","Mar(0)","Apr(0)","May(0)","Jun(0)", \
              "Jul(0)","Aug(0)","Sep(0)","Oct(0)","Nov(0)","Dec(0)", \
              "Jan(+1)","Feb(+1)","Mar(+1)","Apr(+1)","May(+1)","Jun(+1)", \
              "Jul(+1)","Aug(+1)","Sep(+1)","Oct(+1)","Nov(+1)","Dec(+1)"]
    tmp1 = ts1.values.reshape([-1,nmon])
    tmp2 = ts2.values.reshape([-1,nmon])
    if nyear == 3:
        ym1 = [c.replace('+','-') for c in calMons[nmon:]]
        calMons = ym1+calMons
        temp1 = np.concatenate([tmp1[:-2,:],tmp1[1:-1,:],tmp1[2:,:]],axis=1)
        temp2 = np.concatenate([tmp2[:-2,:],tmp2[1:-1,:],tmp2[2:,:]],axis=1)
    else:
        temp1 = np.concatenate([tmp1[:-1,:],tmp1[1:,:]],axis=1)
        temp2 = np.concatenate([tmp2[:-1,:],tmp2[1:,:]],axis=1)
    #print(temp1[:,:-offset+endMon].shape)
    #print(temp2[:,offset:endMon].shape)
    #print(len(calMons[offset:endMon]))
    if lstd: temp1 = temp1/temp1.std(axis=0)  # Standardise ts1 only
    df_stats = pd.Series(sfunc(temp1[:,:-offset+endMon],temp2[:,offset:endMon]),index=calMons[offset:endMon])
    return df_stats

def lagClimStat_sr (ts1,ts2,offset=2,endMon=-7,lstat='reg',lstd=False,nyear=2):
    """ Calculate lagged climatological regression/correlation between two pandas series. 
    The calculations are useful for ENSO-related analysis.

    Inputs:
        ts1 = Series 1
        ts2 = Series 2
        offset = Start (calendar) month or offset for ts2 w.r.t. ts1 (default = 2 [March])
        endMon = End (calendar) month, from the end of the second calendar year (default = -7 [May(+1)])
        lstat = Regression or correlation
        lstd =  If true, standardise ts1
        nyear = Lagged climatology for 2 or 3 years
    """
    #if not isinstance(ts1,pd.Series) and not isinstance(ts2,pd.Series):
    #   print('Both inputs must be pd.Series')
    #   return 
    if np.ndim(ts1) != 1 or np.ndim(ts2) != 1:
       print('Both inputs must be 1-d series')
       return 

    if endMon == 0: endMon = -1
    if endMon > 0:  endMon = -1*endMon
    if lstat == 'reg':
        sfunc = simpReg
    else:
        sfunc = simpCorr

    temp1 = lagClimMons_sr (ts1,nyear=nyear)
    temp2 = lagClimMons_sr (ts2,nyear=nyear)
    #calMons = temp1.columns
    if lstd: temp1 = temp1/temp1.std(axis=0)  # Standardise ts1 only
    df_stats = sfunc(temp1.iloc[:,:-offset+endMon],temp2.iloc[:,offset:endMon])
    if lstat == 'reg':
        df_stats = df_stats['RegCoeff']

    return df_stats

def lagClimStat (ts1,ts2,offset=2,endMon=-7,lstat='reg',lstd=False,nyear=2):
    """ Calculate lagged climatological regression/correlation between two pandas series. 
    The calculations are useful for ENSO-related analysis.

    Inputs:
        ts1 = Series/DataFrame 1
        ts2 = Series/DataFrame 2
        offset = Start (calendar) month or offset for ts2 w.r.t. ts1 (default = 2 [March])
        endMon = End (calendar) month, from the end of the second calendar year (default = -7 [May(+1)])
        lstat = Regression or correlation
        lstd =  If true, standardise ts1
        nyear = Lagged climatology for 2 or 3 years
    """

    #if isinstance(ts1,pd.Series) and isinstance(ts2,pd.Series):
    if np.ndim(ts1) == np.ndim(ts2) == 1:
        return lagClimStat_sr (ts1,ts2,offset=offset,endMon=endMon,lstat=lstat,lstd=lstd,nyear=nyear)

    if isinstance(ts2,pd.DataFrame):
        cols = ts2.columns
        df_stats = pd.DataFrame(columns = cols)
        if ts1.shape == ts2.shape:
            for i,col in enumerate(cols):
                df_stats[col] = lagClimStat_sr (ts1.iloc[:,i],ts2[col],offset=offset,endMon=endMon,lstat=lstat,lstd=lstd,nyear=nyear)
        elif np.ndim(ts1) == 1:
            for col in cols:
                df_stats[col] = lagClimStat_sr (ts1,ts2[col],offset=offset,endMon=endMon,lstat=lstat,lstd=lstd,nyear=nyear)
        return df_stats
    else:
        print('For 2-d arrays, both must be DataFrames (of the same shape)!')
        return

def lagStatsENSO_sr (ts1,ts2,peak_mon='Dec(0)',lstat='reg',lstd=False,nyear=2):
    """ Calculate lagged regression/correlation between two pandas series for ENSO growth 
    and decay phases. The calculations are useful for ENSO-related analysis.

    Inputs:
        ts1 = Series 1 (usually, December SSTAs when ENSO peaks in Obs)
        ts2 = Series 2 (SST or any other TS that correlates with SST)
        peak_mon = The month of ENSO peak in obs/models (e.g., 'Dec(0)')
        lstat = Regression or correlation
        lstd =  If true, standardise ts1
        nyear = Lagged climatology for 2
    """
    if np.ndim(ts1) != 1 or np.ndim(ts2) != 1:
       print('Both inputs must be 1-d series')
       return 

    if lstat == 'reg':
        sfunc = simpReg
    else:
        sfunc = simpCorr

    temp1 = lagClimMons_sr (ts1,nyear=nyear)[peak_mon]
    temp2 = lagClimMons_sr (ts2,nyear=nyear)
    #calMons = temp1.columns
    if lstd: temp1 = temp1/temp1.std(axis=0)  # Standardise ts1 only
    df_stats = sfunc(temp1,temp2)
    #if hasattr(df_stats,'RegCoeff'):
    if lstat == 'reg':
        df_stats = df_stats['RegCoeff']

    return df_stats

def lagStatsENSO (ts1,ts2,peak_mon='Dec(0)',lstat='reg',lstd=False,nyear=2):
    """ Calculate lagged regression/correlation between two pandas series/dataframe for ENSO growth
    and decay phases. The calculations are useful for ENSO-related analysis.

    Inputs:
        ts1 = Series/DataFrame 1 (usually, December SSTAs when ENSO peaks in Obs)
        ts2 = Series/DataFrame 2 (SST or any other TS that correlates with SST)
        peak_mon = The month of ENSO peak in obs/models (e.g., 'Dec(0)')
        lstat = Regression or correlation
        lstd =  If true, standardise ts1
        nyear = Lagged climatology for 2
    """

    #if isinstance(ts1,pd.Series) and isinstance(ts2,pd.Series):
    if np.ndim(ts1) == np.ndim(ts2) == 1:
        return lagStatsENSO_sr (ts1,ts2,peak_mon=peak_mon,lstat=lstat,lstd=lstd,nyear=nyear)

    if isinstance(ts2,pd.DataFrame):
        cols = ts2.columns
        df_stats = pd.DataFrame(columns = cols)
        if ts1.shape == ts2.shape:
            for i,col in enumerate(cols):
                df_stats[col] = lagStatsENSO_sr (ts1.iloc[:,i],ts2[col],peak_mon=peak_mon,lstat=lstat,lstd=lstd,nyear=nyear)
        elif np.ndim(ts1) == 1:
            for col in cols:
                df_stats[col] = lagStatsENSO_sr (ts1,ts2[col],peak_mon=peak_mon,lstat=lstat,lstd=lstd,nyear=nyear)
        return df_stats
    else:
        print('For 2-d arrays, both must be DataFrames (of the same shape)!')
        return

def pspecthp(A, C, nfft=512, nsampf=1):
    """USAGE (matlab): [freq0, spec, G] = pspecthp(A,C,nfft,nsampf)
    PSPECTHD  Calculates theoretically the power spectra and coherence 
           spectrum of a discrete multi-variate process. The relevant
           formulas are given on pages 474 (Eq 11.2.28) and 355 of Jenkins 
           and Watts (1968). See also page 238 of Storch and Zwiers (1999).

        See pspecthd.m for the special case of bivariate processes.

        On input:
           A -> Estimated VAR(p) coefficient matrix
           C -> (co)-variances of the residuals of the two variables
           nfft -> Number of frequencies at which spectrum to be estimated (default=512)
           nsampf -> Sampling frequency => Inverse of time interval (in days/months/years) 
                          (default = 1 per time unit)
        On output:
           spec -> calculated power and coherence spectra
           freq -> frequencies at which calculations are made
           G    -> spectral-and-cross spectral matrix. Diagonal elements
                   of G are auto-spectra and the off-diagonal elements 
                   are cross spectra.

    Matlab VERSION  Harun Rashid  20-MAY-2003
    Python version H Rashid 11-JUL-2023 (Translation of ~/matlab/mfiles/myfiles/pspecthp.m)

    Python version is verified against the matlab version in test_pspecthp.py
    """

    #if len(A.shape) != 2 or A.shape[0] != A.shape[1]:
    #    raise ValueError("A must be a square matrix")

    pord, na, na = A.shape

    if C.shape[0] != C.shape[1] or C.shape[0] != na:
        raise ValueError("C must be a square matrix")

    if nsampf < 0.5:
        print("Warning: nsampf < 0.5; there may be an error!")

    if nfft < 129:
        print("Warning: nfft < 129; there may be an error!")

    freq = np.arange(0, 1/2 + 1/nfft, 1/nfft)
    
    A1 = np.zeros((na, na), dtype=np.complex128)
    G = np.zeros((na, na, nfft//2 + 1), dtype=np.complex128)
    
    for ifrq in range(nfft//2 + 1):
        H1inv = np.eye(na, dtype=np.complex128)
        H2inv = np.eye(na, dtype=np.complex128)
        for ima in range(1,pord+1):
            A1[:] = A[ima-1]
            H1inv -= A1 * np.exp(1j * 2 * np.pi * ima * freq[ifrq]) # check if ima+1 here and below
            H2inv -= A1.T * np.exp(-1j * 2 * np.pi * ima * freq[ifrq])
        G[:,:,ifrq] = np.linalg.inv(H1inv) @ C @ np.linalg.inv(H2inv)

    spec1 = np.real(G[0, 0, :]) 
    spec2 = np.real(G[1, 1, :])
    cross = G[0, 1, :]
    coh = np.abs(cross)**2 / (spec1 * spec2) # compensate for multiples of 2 above by multiplying by 4
    freq *= nsampf

    return freq, 2*spec1, 2*spec2, coh  # multiply by 2, as only the real part is returned
    #return freq, 2*spec1, 2*spec2, coh, G  #  For debugging

def compIndexFm (tas, indx=None):
    """Calculate spatially-averaged climate indices from SAT field. The last two dims 
    are assumed (lat,lon). Selected indices may be calculated, as opposed to all. tas 
    can have missing values. 

    Input:
       tas => a 3-d SAT or any other fields.
    Output:
       xr_inds => An xarray DataArray with (ntime,nindex) dimensions.

    HAR - 18 Oct 2023
    """
    import xarray as xr

    dims = tas.dims
    if tas[dims[-1]].values[0] < 0:
        tas = lonFlip(tas)
    if tas[dims[-2]].values[0] > tas[dims[-2]].values[1]:   # lat: N->S
        tas = tas[:,::-1,:] # Make lats S->N

    latS = tas[dims[-2]].values[0]
    latN = tas[dims[-2]].values[-1]
    lonW = tas[dims[-1]].values[0]
    lonE = tas[dims[-1]].values[-1]

    dict_coords = {'Glob': [latS, latN, lonW, lonE],
     'Trop': [-20.0, 20.0, lonW, lonE],
     'NH': [20.0, latN, lonW, lonE],
     'SH': [latS, -20.0, lonW, lonE],
     'Nino3.4': [-5.0, 5.0, 190.0, 240.0],
     'Nino3': [-5.0, 5.0, 210.0, 270.0],
     'Nino4': [-5.0, 5.0, 160.0, 210.0],
     'Nino1': [-10.0, -5.0, 270.0, 280.0],
     'Nino2': [-5.0, 0.0, 270.0, 280.0],
     'WarmPool': [-5.0, 0.0, 160.0, 200.0],
     'IODW': [-10.0, 10.0, 50.0, 70.0],
     'IODE': [-10.0, 0.0, 90.0, 110.0],
     'CTI': [-5.0, 5.0, 180.0, 270.0],
     'NASST': [0.0, 60.0, 285.0, 352.5],
     'TPI-N': [25.0, 45.0, 140.0, 215.0],
     'TPI-T': [-10.0, 10.0, 170.0, 270.0],
     'TPI-S': [-50.0, -15.0, 150.0, 200.0],
     'AUS': [-45.0,-10.0,112.5,155.62]}

    regNames = indx
    if indx is None:
        regNames = ['Glob','Trop','NH','SH','Nino3','Nino3.4','Nino4','IOD','TPI','NASST','AUS']
    elif not isinstance(indx,list):
        regNames = [indx]

    dict_temp = {}
    if 'IOD' in regNames:
        for reg in ['IODW','IODE']:
            v = dict_coords[reg]
            if dims[-2] == 'lat':
                dict_temp[reg] = wgt_meanm(tas.sel(lat=slice(v[0],v[1]),lon=slice(v[2],v[3])))
            else:
                dict_temp[reg] = wgt_meanm(tas.sel(latitude=slice(v[0],v[1]),longitude=slice(v[2],v[3]))) 
    if 'TPI' in regNames:
        for reg in ['TPI-N','TPI-T','TPI-S']:
            v = dict_coords[reg]
            if dims[-2] == 'lat':
                dict_temp[reg] = wgt_meanm(tas.sel(lat=slice(v[0],v[1]),lon=slice(v[2],v[3])))
            else:
                dict_temp[reg] = wgt_meanm(tas.sel(latitude=slice(v[0],v[1]),longitude=slice(v[2],v[3])))

    list_inds = []
    for reg in regNames:
        if reg == 'IOD':
            list_inds.append(dict_temp['IODW']-dict_temp['IODE'])
        elif reg == 'TPI':
            list_inds.append(dict_temp['TPI-T']-(dict_temp['TPI-N']+dict_temp['TPI-S'])/2)
        else:
            v = dict_coords[reg]
            if dims[-2] == 'lat':
                list_inds.append(wgt_meanm(tas.sel(lat=slice(v[0],v[1]),lon=slice(v[2],v[3]))))
            else:
                list_inds.append(wgt_meanm(tas.sel(latitude=slice(v[0],v[1]),longitude=slice(v[2],v[3]))))

    #xr_inds = xr.concat(list_inds,dim='indx').T
    nregs = len(regNames)
    xr_inds = xr.DataArray(list_inds,dims=('indx','time'),coords={'indx':np.arange(nregs),'time':tas.time})
    xr_inds.attrs['name'] = 'clim_inds'
    if hasattr(tas,'units'): xr_inds.attrs['units'] = tas.units
    if hasattr(tas,'long_name'): xr_inds.attrs['long_name'] = "Spatially averaged climate indices of "+tas.long_name
    xr_inds.coords['indx'] = regNames
    xr_inds.coords['indx'].attrs['long_name'] = "Climate indices"

    #df=xr_inds.to_pandas()
    return xr_inds

def compIndexF (tas, indx=None):
    """Calculate spatially-averaged climate indices from SAT field. The last two dims 
    are assumed (lat,lon). Selected indices may be calculated, as opposed to all. This
    (and wgt_areaave) appear to handle missing values (more testing needed?) as well 
    as compIndexFm. This is slightly faster.

    Input:
       tas => a 3-d SAT or any other fields.
    Output:
       xr_inds => An xarray DataArray with (ntime,nindex) dimensions.

    HAR - 18 Oct 2023
    """
    import xarray as xr

    dims = tas.dims
    if tas[dims[-1]].values[0] < 0:
        tas = lonFlip(tas)
    if tas[dims[-2]].values[0] > tas[dims[-2]].values[1]:   # lat: N->S
        tas = tas[:,::-1,:] # Make lats S->N

    latS = tas[dims[-2]].values[0]
    latN = tas[dims[-2]].values[-1]
    lonW = tas[dims[-1]].values[0]
    lonE = tas[dims[-1]].values[-1]

    dict_coords = {'Glob': [latS, latN, lonW, lonE],
     'Trop': [-20.0, 20.0, lonW, lonE],
     'NH': [20.0, latN, lonW, lonE],
     'SH': [latS, -20.0, lonW, lonE],
     'Nino3.4': [-5.0, 5.0, 190.0, 240.0],
     'Nino3': [-5.0, 5.0, 210.0, 270.0],
     'Nino4': [-5.0, 5.0, 160.0, 210.0],
     'Nino1': [-10.0, -5.0, 270.0, 280.0],
     'Nino2': [-5.0, 0.0, 270.0, 280.0],
     'WarmPool': [-5.0, 0.0, 160.0, 200.0],
     'IODW': [-10.0, 10.0, 50.0, 70.0],
     'IODE': [-10.0, 0.0, 90.0, 110.0],
     'CTI': [-5.0, 5.0, 180.0, 270.0],
     'NASST': [0.0, 60.0, 285.0, 352.5],
     'TPI-N': [25.0, 45.0, 140.0, 215.0],
     'TPI-T': [-10.0, 10.0, 170.0, 270.0],
     'TPI-S': [-50.0, -15.0, 150.0, 200.0],
     'AUS': [-45.0,-10.0,112.5,155.62]}

    regNames = indx
    if indx is None:
        regNames = ['Glob','Trop','NH','SH','Nino3','Nino3.4','Nino4','IOD','TPI','NASST','AUS']
    elif not isinstance(indx,list):
        regNames = [indx]

    #sidx = [r for r in dict_coords.keys() if 'IOD' in r or 'TPI' in r]
    dict_temp = {}
    if 'IOD' in regNames:
        for reg in ['IODW','IODE']:
            v = dict_coords[reg]
            if dims[-2] == 'lat':
                dict_temp[reg] = wgt_areaave(tas.sel(lat=slice(v[0],v[1]),lon=slice(v[2],v[3])))
            else:
                dict_temp[reg] = wgt_areaave(tas.sel(latitude=slice(v[0],v[1]),longitude=slice(v[2],v[3]))) 
    if 'TPI' in regNames:
        for reg in ['TPI-N','TPI-T','TPI-S']:
            v = dict_coords[reg]
            if dims[-2] == 'lat':
                dict_temp[reg] = wgt_areaave(tas.sel(lat=slice(v[0],v[1]),lon=slice(v[2],v[3])))
            else:
                dict_temp[reg] = wgt_areaave(tas.sel(latitude=slice(v[0],v[1]),longitude=slice(v[2],v[3])))

    list_inds = []
    for reg in regNames:
        if reg == 'IOD':
            list_inds.append(dict_temp['IODW']-dict_temp['IODE'])
        elif reg == 'TPI':
            list_inds.append(dict_temp['TPI-T']-(dict_temp['TPI-N']+dict_temp['TPI-S'])/2)
        else:
            v = dict_coords[reg]
            if dims[-2] == 'lat':
                list_inds.append(wgt_areaave(tas.sel(lat=slice(v[0],v[1]),lon=slice(v[2],v[3]))))
            else:
                list_inds.append(wgt_areaave(tas.sel(latitude=slice(v[0],v[1]),longitude=slice(v[2],v[3]))))

    #xr_inds = xr.concat(list_inds,dim='indx').T
    nregs = len(regNames)
    xr_inds = xr.DataArray(np.array(list_inds),dims=('indx','time'),coords={'indx':np.arange(nregs),'time':tas.time})
    xr_inds.attrs['name'] = 'clim_inds'
    if hasattr(tas,'units'): xr_inds.attrs['units'] = tas.units
    if hasattr(tas,'long_name'): xr_inds.attrs['long_name'] = "Spatially averaged climate indices of "+tas.long_name
    xr_inds.coords['indx'] = regNames
    xr_inds.coords['indx'].attrs['long_name'] = "Climate indices"

    #df=xr_inds.to_pandas()
    return xr_inds

def r_pvalues(df,corr=False):
    """
     Function to calculate p-values for each pairwise correlation coefficient.
     From: https://scales.arabpsychology.com/stats/how-to-calculate-the-p-value-for-a-correlation-coefficient-in-pandas/#google_vignette

    Return a matrix of p-values if corr==False, else return the correlation matrix [df.corr() is faster] 
    """

    #cols = pd.DataFrame(columns=df.columns)
    #p = cols.transpose().join(cols, how='outer')
    p = pd.DataFrame(index=df.columns,columns=df.columns)

    for c in df.columns:
        for r in df.columns:
            tmp = df[df[r].notnull() & df[c].notnull()]
            if corr:
                #p[r][c] = scipy.stats.pearsonr(tmp[r], tmp[c])[0]
                p.loc[r,c] = scipy.stats.pearsonr(tmp[c], tmp[r])[0]
            else:
                #p[r][c] = scipy.stats.pearsonr(tmp[r], tmp[c])[1]
                p.loc[r,c] = scipy.stats.pearsonr(tmp[c], tmp[r])[1]

    return p

def comp_thermoclineDepth (thzx,zaxis='lev',nlev=500):
    """
    Computations of thermocline depth, the maximum gradient of ocean
    temperature profiles at different longitudes. As the ENSO-related 
    thermocline variability occurs near the equator, the temp is averaged
    over -0.5,0.5 latitudes. The steps of computations are:
    1) Interpolate temp values from curvilinear grid to a
       1x1 degree regular grid using CDO (before passing into this function)
    2) Take lat average over -0.5,0.5 degrees (before passing into this function)
    3) Interpolate to a finer vertical level coordinate using 
       the cubic interpolation method. The linear interpolation
       isn't useful in this case, as we want to determine the
       depth of max temp grad and linear interpolation gives const.
       gradients between the interpolated values
    4) Differentiate along vertical coordinate
    5) Determine the depth at which the gradient is a maximum
    6) Finally, smooth slightly in longitudes using a 5-point rolling
       mean.
    7) Repeat above for different netCDF files and ensemble members of
       a CMIP experiment.

    The input thetao must be a 3-d array (time,lev,lon). A few pre-processing
    steps (for CMIP outputs) will help prepare this input data.

    a) Do horizontal inerpolation to a lat-lon coordinate
    b) Select the equatorial data (-0.5,0.5) [see point 2) above)
    c) Do the latitude averaging

      subprocess.run("cdo -L mermean -sellonlatbox,0.,360,-0.5,0.5 -remapbil,r360x180 "+inFile+" "+outFile,shell=True)

    d) Do time merging of individual files before or after the above

    Input:
       thzx (time,lev,lon) - Input lat-averaged (-0.5,0.5) ocean temperature (thetao; xarray.DataArray)

    Output:
       thermo_depth (time,lon) - Thermocline depth along the equator (xarray.DataArray)

    This version:
    Harun Rashid
    30-MAY-2024
    """
    import xarray as xr
   
    lev0 = thzx.lev
    lev = np.linspace(lev0[0],lev0[-1],nlev)
    num_miss = thzx[0].count(dim=zaxis).values
    thf = xr.DataArray(dims=('time','lev','lon'),coords={'time':thzx.time,'lev':lev,'lon':thzx.lon})
    for i,n in enumerate(num_miss):
        if n > 3:  # minimum 3 non-missing data needed for cubic interpolation
            thf[:,:,i] = thzx[:,:,i].dropna(zaxis).interp(lev=lev,method='cubic').values
        else:
            thf[:,:,i] = np.nan
    dtdz = thf.differentiate(zaxis)   # %timeit => 6.96 s
    thermo_depth = dtdz.idxmin(dim=zaxis)
    thermo_depth = thermo_depth.rolling(lon=5, center=True).mean()
    return thermo_depth

def diag_table_df (df_data, ufld='UAS4'):
    """ Calculates ENSO related metrics from input Nino sea surface temperatures (SSTs), 
    zonal wind stress (TAUU), and thermoclice depth (THCD) data. This function is for
    single realisations only (e.g., obs or an individual simulation). For multiple
    ensemble simulations, use diag_table or diag_table_ens.

    NB: The columns names are assumed to be: 'SST3','TAUU/UAS4','THCD','SST4' (in any order).
    Inputs:
        df_data - pd.DataFrame with the following columns:
           SST3 - Nino-3 SST data (full data, not anomalies)
           SST34 - Nino-3.4 SST data
           SST4 - Nino-4 SST data
           TAUU - Nino-4 zonal wind stress data, or
           UAS4 - Nino-4 surface zonal winds
           THCD - Equatorial Pacific (-0.5,0.5; 124-277) averaged thermoclice depth data
           QNET3- Net surface heatfux in the Nino-3 region
           PR34 - Precip in the Nino-3.4 region

    This function is for a DataFrame and operates on its columns. Use diag_table_ens to
    calculate separate diagnostics sets for each member of an ensemble of models.

    ---
    Harun Rashid
    09-SEP-2024
    05-MAY-2025 [Code reorganised as blocks for optional variables (THCD,PR,UFLD,QNET);
                 renamed: diag_table_sr->diag_table_df]
    """

    df_data_mean = df_data.mean()
    df_data_ano = anomaly_df(detrend_df(df_data,2))
    df_pos,df_neg = comp_Stats(df_data_ano['SST3'].squeeze())
    df_data_std = df_data_ano.std()
    df_data_ano_std = df_data_ano/df_data_std
    df_data_ano_stdac = df_data_ano['SST3'].groupby(df_data_ano.index.month).std()
    df_data_ts_spec = spectrum(df_data_ano['SST3'],19)
    df_data_ts_spec.index *= 12  # cyc/year
    df_spc1 = df_data_ts_spec.loc[1/8:1/2]               # 2-8 year periods for ENSO

    df_diag = {}
    df_diag['SST3mean'] = df_data_mean['SST3']
    df_diag['SST34mean'] = df_data_mean['SST34']
    df_diag['SST4mean'] = df_data_mean['SST4']
    df_diag['SSTdiff'] = df_data_mean['SST4'] - df_data_mean['SST3'] # -ve of SST gradient
    df_diag['SST3stdv'] = df_data_std['SST3']
    df_diag['SST34stdv'] = df_data_std['SST34']
    df_diag['SST4stdv'] = df_data_std['SST4']
    df_diag['PhaseLockRange'] = df_data_ano_stdac.max()-df_data_ano_stdac.min()
    df_diag['PhaseLockMaxMon'] = df_data_ano_stdac.idxmax()
    df_diag['PhaseLockMinMon'] = df_data_ano_stdac.idxmin()
    df_diag['SST3skew'] = df_data_ano['SST3'].skew()
    df_diag['ENSOpeakPeriod'] = 1/df_data_ts_spec.idxmax()
    df_diag['ENSOtimeScale'] = 1/((df_spc1*df_spc1.index).sum(axis=0)/df_spc1.sum(axis=0))

    df_diag['EN_Duration'] = df_pos['Durations'].mean()
    df_diag['LN_Duration'] = df_neg['Durations'].mean()
    df_diag['EN_MaxVal'] = df_pos['MaxMinval'].mean()
    df_diag['LN_MinVal'] = df_neg['MaxMinval'].mean()

    if 'THCD' in df_data.columns:
        df_reg_mtd_ts = lagReg(df_data_ano['THCD'],df_data_ano['SST3'],20)[0]
        df_diag['TCDmean'] = df_data_mean['THCD']
        df_diag['TCDstdv'] = df_data_std['THCD']
        max_ind = df_reg_mtd_ts.idxmax()   # Only +ve lags are relevant for the forcing/feedbacks
        df_diag['ThermoclineFdbk'] = df_reg_mtd_ts.loc[max_ind]
        df_diag['maxLag_TCFdbk'] = max_ind
    if 'THCD3' in df_data.columns:
        df_reg_mtd_ts = lagReg(df_data_ano['THCD3'],df_data_ano['SST3'],20)[0]
        df_diag['TCD3mean'] = df_data_mean['THCD3']
        df_diag['TCD3stdv'] = df_data_std['THCD3']
        max_ind = df_reg_mtd_ts.idxmax()   # Only +ve lags are relevant for the forcing/feedbacks
        df_diag['ThermoclineFdbk3'] = df_reg_mtd_ts.loc[max_ind]
        df_diag['maxLag_TCFdbk3'] = max_ind
    if 'THCD4' in df_data.columns:
        df_reg_mtd_ts = lagReg(df_data_ano['THCD4'],df_data_ano['SST3'],20)[0]
        df_diag['TCD4mean'] = df_data_mean['THCD4']
        df_diag['TCD4stdv'] = df_data_std['THCD4']
        max_ind = df_reg_mtd_ts.idxmax()   # Only +ve lags are relevant for the forcing/feedbacks
        df_diag['ThermoclineFdbk4'] = df_reg_mtd_ts.loc[max_ind]
        df_diag['maxLag_TCFdbk4'] = max_ind

    if ufld in df_data.columns:
        df_reg_ufld_ts = lagReg(df_data_ano[ufld],df_data_ano['SST3'],10)[0]
        df_reg_ts_ufld = lagReg(df_data_ano['SST3'],df_data_ano[ufld],10)[0]
        df_diag[ufld+'mean'] = df_data_mean[ufld]
        df_diag[ufld+'stdv'] = df_data_std[ufld]
        if ufld[:-1]+'34' in df_data.columns:
            df_diag[ufld[:-1]+'34mean'] = df_data_mean[ufld[:-1]+'34']
            df_diag[ufld[:-1]+'34stdv'] = df_data_std[ufld[:-1]+'34']
        max_ind = df_reg_ts_ufld.idxmax()
        df_diag['BjerknessFdbk'] = df_reg_ts_ufld.loc[0]
        df_diag['maxLag_BJFdbk'] = max_ind
        max_ind = df_reg_ufld_ts.idxmax()
        df_diag['ZonalWindForc'] = df_reg_ufld_ts.loc[max_ind]
        df_diag['maxLag_ZWForc'] = max_ind

    if 'QNET3' in df_data.columns:
        df_diag['QNET3mean'] = df_data_mean['QNET3']
        df_diag['QNET34mean'] = df_data_mean['QNET34']
        df_diag['QNET3stdv'] = df_data_std['QNET3']
        i1 = df_data['QNET3'].first_valid_index()
        df_reg_qnet_ts = lagReg(df_data_ano.loc[i1:,'QNET3'],df_data_ano.loc[i1:,'SST3'],10)[0]
        df_reg_ts_qnet = lagReg(df_data_ano.loc[i1:,'SST3'],df_data_ano.loc[i1:,'QNET3'],10)[0]
        max_ind = df_reg_ts_qnet.idxmax()
        df_diag['ThermodynFdbk'] = df_reg_ts_qnet.loc[0]
        df_diag['maxLag_TDFdbk'] = max_ind
        max_ind = df_reg_qnet_ts.idxmax()
        df_diag['ThermodynForc'] = df_reg_qnet_ts.loc[max_ind]
        df_diag['maxLag_TDForc'] = max_ind

    if 'PR34' in df_data.columns:
        df_diag['PR34mean'] = df_data_mean['PR34']
        df_diag['PR34stdv'] = df_data_std['PR34']
        i1 = df_data['PR34'].first_valid_index()
        if ufld in df_data.columns:
            df_corr_ufld_pr = lagCorr1(df_data_ano.loc[i1:,ufld],df_data_ano.loc[i1:,'PR34'],10)
            max_ind = df_corr_ufld_pr.idxmax()
            df_diag['Corr_'+ufld+'_PR34'] = df_corr_ufld_pr.loc[max_ind]
            df_diag['maxLag_Corr_'+ufld+'_PR34'] = max_ind

    df_metrics = pd.Series(df_diag,dtype='float')

    return df_metrics

def dofCorr (ts1,ts2,nlag=None,dt=1):
    """
    A python function to determine Degrees of Freedom (dof) and the correlation
    coefficient significant at 95% and 99% levels. This is a translation of my
    FORTRAN subroutine 'corrsig.f', except the last few lines of that
    subroutine.

    Translated from my matlab function corrsig.m

    Refs (NCL):
    xydof1 = ntim/(1+2*dim_sum(nmtau*xyacc)/ntim)  Eq. B12 of Oort and Yienger (1996) 
             Note: there is a typo in Eq. 11 of this paper
    xydof2 = ntim/(1+2*sum(xyacc))     page 67 in my thesis [Eqs. 6.2, 6.3]
    xydof3 = ntim*(1-xp*yp)/(1+xp*yp)  Eq. 31 of Bretherton et al. (1999)

    20-SEP-2024  Harun Rashid
    """

    #if len(ts1.shape) != 1:
    #    print('This function can handle only one TS at present')
    if len(ts1) != len(ts2):
        print('Unequal length of the time series')
        return

    if nlag is None:
        nlag = len(ts1)//3

    #acf1 = xcorr(ts1,nlag=nlag) 
    #acf2 = xcorr(ts2,nlag=nlag)
    acf1 = lagCorr(ts1,ts1,nlag) 
    acf2 = lagCorr(ts2,ts2,nlag)

    if isinstance(acf1,pd.Series) and hasattr(acf2,'dims'):
        acf1 = acf1.to_xarray()
        acf1 = acf1.rename({'index':acf2.dims[0]}) 
    #sumacf = (acf1*acf2).sum(acf2.dims[0])
    if hasattr(acf2,'dims'):    # xarray
        sumacf = (acf1*acf2).sum(acf2.dims[0])
    elif hasattr(acf2,'index'): # pandas
        sumacf = (acf2.mul(acf1,axis=0)).sum(axis=0)
    else:                       # numpy
        sumacf = (np.broadcast_to(acf1, acf2.T.shape).T*acf2).sum(axis=0)
    tau = (1.0 + 2.0*np.maximum(0,sumacf))*dt  # make sure all values are +ve
    dof = np.round(len(ts1)*dt/tau)

    return dof

def dofCorr1 (ts1,ts2):
    """
    A python function to determine Degrees of Freedom (dof). This uses lag1 acfs to
    calculate dof (xydof3 below) following Eq. 31 of Bretherton et al. (1999)

    Refs (NCL):
    xydof1 = ntim/(1+2*dim_sum(nmtau*xyacc)/ntim)  Eq. B12 of Oort and Yienger (1996) 
             Note: there is a typo in Eq. 11 of this paper
    xydof2 = ntim/(1+2*sum(xyacc))     page 67 in my thesis [Eqs. 6.2, 6.3]
    xydof3 = ntim*(1-acf1*acf2)/(1+acf1*acf2)  Eq. 31 of Bretherton et al. (1999)

    20-SEP-2024  Harun Rashid
    """

    ntim = len(ts1)
    if ts1.ndim > 1 and ts1.ndim != ts2.ndim:
        print("x must be 1-d or x.ndim == y.ndim!")
        return
    if ntim != len(ts2):
        print('Unequal length of the time series')
        return

    nlag = 1
    acf1 = lagCorr(ts1,ts1,nlag).loc[nlag] 
    acf2 = lagCorr(ts2,ts2,nlag).loc[nlag]

    dof = ntim*(1-acf1*acf2)/(1+acf1*acf2)
    return np.floor(dof)

def sigCorr (dof=100):
    """Compute the corr. coeff. significant at 95% and 99% confidence levels. 
    See Wilks, 1995; Bendat and Piersol, 1971 [pp 126], 1986.

    Return values of statistically signidficant correlation coefficients at 0.05 and 0.01
    p values with 'dof' degrees of freedom.  

    Translated from my matlab function corrsig.m

    19-SEP-2024  Harun Rashid
    """
    #df = dof - 3
    df = dof
    z95 = 1.96/np.sqrt(df)
    r95 = (np.exp(2.0*z95)-1.0)/(np.exp(2.0*z95)+1.0)
    z99 = 2.575/np.sqrt(df)
    r99 = (np.exp(2.0*z99)-1.0)/(np.exp(2.0*z99)+1.0)
    return {'0.05':r95,'0.01':r99} 

def sigReg (xi,yi,regc=None,nlag=1):
    """Compute regression coefficients and their p-values using a two-sided Student-t distribution.
    Take the serial correlation of the input data in calculating the degrees of freedom (DOF). 

    Inputs:
       xi => Independent variable: 1-d or n-d xarrays (should work for numpy arr; not tested for DataFrame)
       yi => Dependent variable: 1-d or n-d xarrays
       regc => pre-computed reg. coeffs (e.g., by simpReg()).
       nlag => time lags used for DOF calculation (in dofCorr())

    Returns regC and p-values or the p-values only.

    21-NOV-2024  Harun Rashid
    """
    assert nlag > 0,'nlag must be a +ve integer!'
    from scipy.stats import t

    if xi.ndim > 1 and xi.ndim != yi.ndim:
        print("x must be 1-d or x.ndim == y.ndim!")
        return

    if regc is None:
        regc = simpRegCorr(xi,yi)
        #regc = simpReg(xi,yi)

    if nlag == 1:
        neff = dofCorr1(xi,yi)
    else:
        neff = dofCorr(xi,yi,nlag)
    resid = regResid(xi,yi)
    std_err = np.sqrt(np.sum(resid**2,axis=0)/(neff-2)) / np.sqrt(np.sum(xi**2,axis=0))
    t_values = regc / std_err
    p_values = t_values.copy()
    p_values[:] = 2 * t.cdf(-abs(t_values), df=neff-2)  # Two-tailed p-value
    if regc is None:
        return regc, p_values
    else:
        return p_values
 
def effective_sample_size(data, lag=1):
    """
    Calculate the effective sample size for a time series, considering lag-1 autocorrelation. 
    The estimated effective sample size may be used for determining the statistical significance 
    of difference of two means.
    
    Parameters:
    - data: array-like, the time series data
    - lag: int, the lag for autocorrelation (default is 1)
    
    Returns:
    - neff: float, the effective sample size
    """
    #from scipy.stats import pearsonr

    n = len(data)
    # Calculate lag-1 autocorrelation
    autocorr = lagCorr(data,data,1).loc[-1]
    #autocorr = pearsonr(data[:-lag], data[lag:])[0]
    # Effective sample size adjustment
    neff = n * (1 - autocorr) / (1 + autocorr)
    return np.maximum(2, neff)  # Ensure neff is at least 1

def significance_of_mean_difference(x, y):
    """
    Calculate the statistical significance of the difference of means between two time series,
    adjusting for serial correlation.
    
    Parameters:
    - x: array-like, first time series data
    - y: array-like, second time series data
    
    Returns:
    - t_stat: float, the calculated t-statistic for the mean difference
    - p_value: float, the p-value for the test
    - significance: bool, whether the difference is statistically significant (p < 0.05)
    """

    from scipy.stats import t

    # Calculate means and variances
    mean_x = np.mean(x, axis=0)
    mean_y = np.mean(y, axis=0)
    var_x = np.var(x, axis=0, ddof=1)
    var_y = np.var(y, axis=0, ddof=1)
    
    # Calculate effective sample sizes
    neff_x = effective_sample_size(x)
    neff_y = effective_sample_size(y)
    #neff_x = len(x) # For test only, should give similar results as t_test_means() below.
    #neff_y = len(y) # This is true, as found in my test (see, plot_LatLonTemp_MinMaxForc_v2.py)

    # Pooled variance, taking effective sample sizes into account
    pooled_variance = (var_x / neff_x) + (var_y / neff_y)
    pooled_variance[:] = np.where(pooled_variance<1e-10,np.nan,pooled_variance)

    # Avoid division by zero in case of very small variances (see above)
    #if pooled_variance == 0:
    #    return np.nan, np.nan
    
    # Calculate t-statistic
    t_stat = (mean_x - mean_y) / np.sqrt(pooled_variance)
    
    # Degrees of freedom for the adjusted sample sizes
    df = neff_x + neff_y - 2
    
    # Two-tailed p-value for the t-test
    p_value = 2 * (1 - t.cdf(abs(t_stat), df))
    
    # Check if the difference is significant at the 95% confidence level
    #significance = p_value < 0.05
    
    return t_stat, p_value

def significance_of_mean(data):
    """
    Calculates the statistical significance of a mean different from zero, 
    taking serial (lag-1) autocorrelation into account.
    
    Parameters:
    - data (array-like): Time series data to test.
    
    Returns:
    - p_value (float): The p-value for the hypothesis test.
    - t_stat (float): The computed t-statistic.
    - effective_n (float): Effective sample size after adjusting for serial correlation.
    """
    from scipy.stats import t

    #data = np.array(data)
    #n = len(data)

    # Step 1: Calculate sample mean and standard deviation
    sample_mean = np.mean(data, axis=0)
    sample_std = np.std(data, axis=0, ddof=1)
    
    # Step 2: Calculate lag-1 autocorrelation
    #autocorrelation = np.corrcoef(data[:-1], data[1:])[0, 1]

    # Step 3: Calculate the effective sample size
    effective_n = effective_sample_size(data)
    #effective_n = n * (1 - autocorrelation) / (1 + autocorrelation)
    effective_n = np.maximum(2, effective_n)  # ensure effective_n is at least 2

    # Step 4: Calculate the standard error with effective sample size
    standard_error = sample_std / np.sqrt(effective_n)

    # Step 5: Calculate t-statistic
    t_stat = sample_mean / standard_error

    # Step 6: Calculate p-value (two-tailed test)
    p_value = 2 * (1 - t.cdf(np.abs(t_stat), df=effective_n - 1))

    return t_stat, p_value

def dofStdErr (x, y):

    """
    USAGE:  prob = dofStdErr(x,y);
       A function to calculate degrees of freedom, t-val, and standard error, needed for
    calculating the statistical significance level of the
    difference of means of two time series. First, a two-sided 't-statistic'
    is computed, and then the corresponding probabilty is calculated from 
    the distribution associated with incomplete beta functions. The quantity
    'prob' calculated in this function gives the probabilty (significance
    level) that the assumed null hypothesis of equal means (of the two time
    series 'x' and 'y') is wrong. A value greater than or equal to 95% means
    that the two time series have means that are significantly different.
       The inputs 'x' and 'y' can be single time series or matrices ('time' as 
    the fist dim) holding multiple (equal) time series. In the latter case 
    'prob' will be a vector of probability values for the different pairs of 
    corresponding time series.

    NOTE: This function is a direct translation of my FORTRAN subroutine
    /bm/gkeep/har/matlab/mfiles/myfiles/compdsig.m. See also:
                atlas:/work13/harun/cd1/ncdfbin/t_test.f

    REFERENCE:
         Zwiers and von Storch, 1995: Taking serial correlation into
                account in tests of the mean. J. Climate, Vol. 8, pp-
                336 - 351.
         Press et al., 1992: Numerical Recipe. CUP.

    NCL version: 08-NOV-2007  M. Harun Ar Rashid
    Python version: 18-Oct-2024  Harun Rashid
    """

    # Get dimensions and ranks of x and y
    dimx = x.shape
    dimy = y.shape
    nx = dimx[0]      # time dim size
    ny = dimy[0]
    if x.ndim > 1:
        mx = np.prod(dimx[1:])
        my = np.prod(dimy[1:])
        dims = dimx[:0]
    else:
        mx, my, dims = 1, 1, 1
    
    # Check if the shapes of x and y match
    if x.ndim != y.ndim or mx != my:
        raise ValueError("The two arrays must have the same shape!")

    # Calculate averages
    avgx = x.mean(axis=0)
    avgy = y.mean(axis=0)
    
    # Remove mean to calculate anomalies
    xdat = x - avgx
    ydat = y - avgy
    
    # Calculate variances
    varx = np.var(x, axis=0, ddof=1)
    vary = np.var(y, axis=0, ddof=1)
    
    # Pooled variance
    varxt = varx * (nx - 1)
    varyt = vary * (ny - 1)
    varpol = (varxt + varyt) / (nx + ny - 2)

    # Autocovariance for lag0
    acvxt = np.sum(xdat[:-1]*xdat[1:], axis=0)
    acvyt = np.sum(ydat[:-1]*ydat[1:], axis=0)
    
    # Lag0 pooled correlation
    varxy = varxt + varyt
    varxy = np.where(np.abs(varxy) < 1.0e-5, 1.0e10, varxy)
    corpol = (acvxt + acvyt) / varxy
    
    # Effective sample sizes
    neffx = np.floor(nx * (1 - corpol) / (1 + corpol))
    neffy = np.floor(ny * (1 - corpol) / (1 + corpol))
    
    # Degrees of freedom
    df = neffx + neffy - 2
    
    # Standard error
    stderr = np.sqrt(varpol) * (1.0 / np.sqrt(neffx) + 1.0 / np.sqrt(neffy))
    #stderr = np.sqrt(varpol) * np.sqrt((1.0 / np.sqrt(neffx)) + (1.0 / np.sqrt(neffy)))
    stderr = np.where(np.abs(stderr) < 1.0e-5, 1.0e10, stderr)
    tval   = (avgy - avgx)/stderr

    return df, tval, stderr

def t_test_means(x, y, equal_var=True):
    """
    Calculates the statistical significance of the difference of means between two samples.
    This doesn't adjust for serial correlation.

    Parameters:
    - x: array-like, sample 1
    - y: array-like, sample 2
    - equal_var: bool, If True, perform a t-test assuming equal variances (default True)

    Returns:
    - t_stat: The computed t-statistic
    - p_value: The p-value associated with the t-test (two-tailed)
    - significance: Whether the difference is statistically significant at 95% confidence level (p < 0.05)
    """
    
    # Perform a two-sample t-test
    t_stat, p_value = sp.stats.ttest_ind(x, y, axis=0, equal_var=equal_var)
    
    # Determine if the difference is statistically significant (p < 0.05)
    #significance = p_value < 0.05
    
    return t_stat, p_value

def t_test_mean_from_zero(sample):
    """
    Calculates the statistical significance of the difference of a sample mean from zero.

    Parameters:
    - sample: array-like, sample data

    Returns:
    - t_stat: The computed t-statistic
    - p_value: The p-value associated with the one-sample t-test (two-tailed)
    - significance: Whether the difference is statistically significant at 95% confidence level (p < 0.05)
    """
    
    # Perform a one-sample t-test against a mean of 0
    t_stat, p_value = sp.stats.ttest_1samp(sample, 0)
    
    # Determine if the difference is statistically significant (p < 0.05)
    #significance = p_value < 0.05
    
    return t_stat, p_value

def chi_square_test_for_variance(sample, hypothesized_variance=1e-10):
    """
    Perform a one-sided chi-square test to check if the sample variance is significantly greater than zero
    (approximated by a small positive value).

    Parameters:
    - sample: array-like, the sample data, with time (usually) as the first dim
    - hypothesized_variance: float, hypothesized variance (must be a small positive value, default is 1e-10)

    Returns:
    - chi2_stat: Chi-square statistic
    - p_value: The p-value for the one-sided chi-square test
    - significance: Whether the variance is significantly greater than the hypothesized value (at 95% confidence level)
    """
    
    # Sample size
    n = len(sample)
    
    # Sample variance
    sample_variance = np.var(sample, axis=0, ddof=1)
    
    # Chi-square statistic calculation
    chi2_stat = (n - 1) * sample_variance / hypothesized_variance
    
    # Degrees of freedom
    df = n - 1
    
    # One-sided p-value for the chi-square test (greater than test)
    p_value = 1 - sp.stats.chi2.cdf(chi2_stat, df)
    
    # Significance check (p < 0.05 for 95% confidence level)
    #significance = p_value < 0.05
    
    return chi2_stat, p_value

