from osgeo import gdal
import numpy as np
from osgeo import osr


#使用gdal.Warp对MODIS数据进行重投影。
modis_lai=gdal.Open(r'D:\DATA\MODIS\LAI\MCD15A3H.A2020181.h13v11.006.2020188204620.hdf')
subdataset_one = modis_lai.GetSubDatasets()[0][0] # 第一个子数据集合
# gdal.Warp(r'D:\code\reprojection.tif', subdataset_one, dstSRS='EPSG:4326')



def reproject(src_file, dst_file, p_width, p_height, epsg_to):
    """
    :param src_file: 输入文件
    :param dst_file: 输出文件
    :param p_width: 输出图像像素宽度
    :param p_height: 输出图像像素高度
    :param epsg_to: 输出图像EPSG坐标代码
    :return:
    """
    # 首先，读取输入数据，然后获得输入数据的投影，放射变换参数，以及图像宽高等信息
    src_ds = gdal.Open(src_file)
    src_srs = osr.SpatialReference()
    src_srs.ImportFromWkt(src_ds.GetProjection())

    srs_trans = src_ds.GetGeoTransform()
    x_size = src_ds.RasterXSize
    y_size = src_ds.RasterYSize

    # 获得输出数据的投影，建立两个投影直接的转换关系
    dst_srs = osr.SpatialReference()
    dst_srs.ImportFromEPSG(epsg_to)
    tx = osr.CoordinateTransformation(src_srs, dst_srs)

    # 计算输出图像四个角点的坐标
    (uly, ulx, _) = tx.TransformPoint(srs_trans[0], srs_trans[3])
    (ury, urx, _) = tx.TransformPoint(srs_trans[0] + srs_trans[1] * x_size, srs_trans[3])
    (lly, llx, _) = tx.TransformPoint(srs_trans[0], srs_trans[3] + srs_trans[5] * y_size)
    (lry, lrx, _) = tx.TransformPoint(srs_trans[0] + srs_trans[1] * x_size + srs_trans[2] * y_size,
                                      srs_trans[3] + srs_trans[4] * x_size + srs_trans[5] * y_size)

    min_x = min(ulx, urx, llx, lrx)
    max_x = max(ulx, urx, llx, lrx)
    min_y = min(uly, ury, lly, lry)
    max_y = max(uly, ury, lly, lry)

    # 创建输出图像，需要计算输出图像的尺寸（重投影以后图像的尺寸会发生变化）
    driver = gdal.GetDriverByName('GTiff')
    dst_ds = driver.Create(dst_file,
                           int((max_x - min_x) / p_width),
                           int((max_y - min_y) / p_height),
                           1, gdal.GDT_Float32)
    dst_trans = (min_x, p_width, srs_trans[2],
                 max_y, srs_trans[4], -p_height)

    # 设置GeoTransform和Projection信息
    dst_ds.SetGeoTransform(dst_trans)
    dst_ds.SetProjection(dst_srs.ExportToWkt())
    # 进行投影转换
    gdal.ReprojectImage(src_ds, dst_ds,
                        src_srs.ExportToWkt(), dst_srs.ExportToWkt(),
                        gdal.GRA_Bilinear)
    dst_ds.GetRasterBand(1).SetNoDataValue(0)  # 设置NoData值
    dst_ds.FlushCache()

    del src_ds
    del dst_ds


reproject(subdataset_one,
          r'D:\code\reprojection2.tif', 0.005, 0.005, 4326)