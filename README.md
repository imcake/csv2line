# OD数据转shp文件
共分为两步：有向流数据转无向流数据和无向流数据转shp文件

## 有向数据转无向数据
需要指定4个变量

1. 有向数据文件名（需是csv文件，不含扩展名）
2. 起点字段名
3. 终点字段名
4. 流量字段名

结果为 有向数据文件名加"_nodirection" 的csv文件

结果字段为OD起终点、流量

## OD数据转shp文件
需要arcgis的arcpy库，需要有3D和Spatial的license。

OD数据中起终点经纬度需要为WGS84坐标系，同时需要将'WGS1984.prj'文件放置在相同目录下，生成shp文件坐标为WGS84坐标系。

若OD数据中起终点数据为其他坐标系，需要将坐标转换为WGS84坐标或者在同目录下防止相应坐标系prj文件，同时修改csv2line.py文件59行，将prj文件名修改为相应文件名。

需要在变量块中修改相应内容

	- path: 工作路径
	- lines: 输出线文件文件名
	- csv_file: 输入csv文件名
	- p1_lng_index: O点经度所在列号
	- p1_lat_index: O点纬度所在列号
	- p2_lng_index: D点经度所在列号
	- p2_lat_index: D点纬度所在列号
	- p1_label_index: O点标签所在列号
	- p2_label_index: D点标签所在列号
	- total_index: 流量所在列号

现有代码转换后的线文件仅附带起点终点和流量三个字段，若需要增加其他字段，需要

1. 37行后的变量块中增加相应字段变量
2. 73行后新增addfile行，添加相应字段名到输出shp文件
3. 76行InsertCursor中增加相应字段名
4. 91行后增加相应变量存储该字段内容在csv文件中的列号
5. 95行增加91行的变量

最终输出文件为ESRI shapefile。