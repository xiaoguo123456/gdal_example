from osgeo import gdal,osr
import netCDF4 as nc
import os
out_path=r'F:\shop\DATA\PET\TIF'

nc_data_path=r'F:\shop\DATA\PET\CN_pet_2010.nc'
nc_data=nc.Dataset(nc_data_path)

for i in range(12):

    output=os.path.join(out_path,os.path.split(nc_data_path)[1].replace('.nc','_'+str(i+1)+'_.tif'))
    data=nc_data.variables['pet'][:][i,:,:]

    driver = gdal.GetDriverByName('Gtiff')
    out_tif = driver.Create(output, data.shape[1], data.shape[0], 1, gdal.GDT_Int32)
    out_tif.SetGeoTransform((min(nc_data.variables['lon'][:]),
                             nc_data.variables['lon'][:][1]-nc_data.variables['lon'][:][0],
                             0,
                             max(nc_data.variables['lat'][:]),
                             0,
                             nc_data.variables['lat'][:][1]-nc_data.variables['lat'][:][0]))
    projection = osr.SpatialReference()
    projection.ImportFromEPSG(4326)
    s = projection.ExportToWkt()
    out_tif.SetProjection(s)
    out_tif.GetRasterBand(1).WriteArray(data)
    del out_tif

