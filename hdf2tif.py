from osgeo import gdal
​
root_ds = gdal.Open('example.hdf')
# 返回结果是一个list，list中的每个元素是一个tuple，每个tuple中包含了对数据集的路径，元数据等的描述信息
# tuple中的第一个元素描述的是数据子集的全路径
ds_list = root_ds.GetSubDatasets()
​
band_1 = gdal.Open(ds_list[11][0])  # 取出第12个数据子集（MODIS反射率产品的第一个波段）
arr_bnd1 = band_1.ReadAsArray()  # 将数据集中的数据转为ndarray
​
# 创建输出数据集，转为GeoTIFF进行写入
out_file = 'sr_band1.tif'
driver = gdal.GetDriverByName('GTiff')
out_ds = driver.CreateCopy(out_file, band_1)
out_ds.GetRasterBand(1).WriteArray(arr_bnd1)
out_ds.FlushCache()
​
# 关闭数据集
out_ds = None
root_ds = None
