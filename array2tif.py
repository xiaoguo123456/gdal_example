import gdal
import numpy as np
import osr

def array2tif(input_file,output):
    """

    :param input_file: .npy file
    :param output: tif file
    :return:
    """
    data=np.load(input_file)
    driver=gdal.GetDriverByName('Gtiff')
    out_tif=driver.Create(output,data.shape[1],data.shape[0],1,gdal.GDT_Int32)
    out_tif.SetGeoTransform((-180,0.05,0,90,0,-0.05))
    projection=osr.SpatialReference()
    projection.ImportFromEPSG(4326)
    s = projection.ExportToWkt()
    out_tif.SetProjection(s)
    out_tif.GetRasterBand(1).WriteArray(data)
    del out_tif

array2tif('ET_MERRA_20170101.npy','test.tif')
